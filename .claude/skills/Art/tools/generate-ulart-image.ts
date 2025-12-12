#!/usr/bin/env bun

/**
 * generate-ulart-image - UL Image Generation CLI
 *
 * Generate Unsupervised Learning branded images using Flux 1.1 Pro, Nano Banana, Nano Banana Pro, or GPT-image-1.
 * Follows llcli pattern for deterministic, composable CLI design.
 *
 * Usage:
 *   generate-ulart-image --model nano-banana-pro --prompt "..." --size 16:9 --output /tmp/image.png
 *
 * @see ${PAI_DIR}/skills/art/README.md
 */

import Replicate from "replicate";
import OpenAI from "openai";
import { GoogleGenAI } from "@google/genai";
import { writeFile, readFile } from "node:fs/promises";
import { extname, resolve } from "node:path";

// ============================================================================
// Environment Loading
// ============================================================================

/**
 * Load environment variables from ${PAI_DIR}/.env
 * This ensures API keys are available regardless of how the CLI is invoked
 */
async function loadEnv(): Promise<void> {
  const envPath = resolve(process.env.HOME!, '.claude/.env');
  try {
    const envContent = await readFile(envPath, 'utf-8');
    for (const line of envContent.split('\n')) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      const eqIndex = trimmed.indexOf('=');
      if (eqIndex === -1) continue;
      const key = trimmed.slice(0, eqIndex).trim();
      let value = trimmed.slice(eqIndex + 1).trim();
      // Remove surrounding quotes if present
      if ((value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))) {
        value = value.slice(1, -1);
      }
      // Only set if not already defined (allow overrides from shell)
      if (!process.env[key]) {
        process.env[key] = value;
      }
    }
  } catch (error) {
    // Silently continue if .env doesn't exist - rely on shell env vars
  }
}

// ============================================================================
// Types
// ============================================================================

type Model = "flux" | "nano-banana" | "nano-banana-pro" | "gpt-image-1";
type ReplicateSize = "1:1" | "16:9" | "3:2" | "2:3" | "3:4" | "4:3" | "4:5" | "5:4" | "9:16" | "21:9";
type OpenAISize = "1024x1024" | "1536x1024" | "1024x1536";
type GeminiSize = "1K" | "2K" | "4K";
type Size = ReplicateSize | OpenAISize | GeminiSize;

interface CLIArgs {
  model: Model;
  prompt: string;
  size: Size;
  output: string;
  creativeVariations?: number;
  aspectRatio?: ReplicateSize; // For Gemini models
  transparent?: boolean; // Enable transparent background
  referenceImage?: string; // Reference image path (Nano Banana Pro only)
  removeBg?: boolean; // Remove background after generation using remove.bg API
}

// ============================================================================
// Configuration
// ============================================================================

const DEFAULTS = {
  model: "flux" as Model,
  size: "16:9" as Size,
  output: "/tmp/ul-image.png",
};

const REPLICATE_SIZES: ReplicateSize[] = ["1:1", "16:9", "3:2", "2:3", "3:4", "4:3", "4:5", "5:4", "9:16", "21:9"];
const OPENAI_SIZES: OpenAISize[] = ["1024x1024", "1536x1024", "1024x1536"];
const GEMINI_SIZES: GeminiSize[] = ["1K", "2K", "4K"];

// Aspect ratio mapping for Gemini (used with image size like 2K)
const GEMINI_ASPECT_RATIOS: ReplicateSize[] = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"];

// ============================================================================
// Error Handling
// ============================================================================

class CLIError extends Error {
  constructor(message: string, public exitCode: number = 1) {
    super(message);
    this.name = "CLIError";
  }
}

function handleError(error: unknown): never {
  if (error instanceof CLIError) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(error.exitCode);
  }

  if (error instanceof Error) {
    console.error(`❌ Unexpected error: ${error.message}`);
    console.error(error.stack);
    process.exit(1);
  }

  console.error(`❌ Unknown error:`, error);
  process.exit(1);
}

// ============================================================================
// Help Text
// ============================================================================

function showHelp(): void {
  console.log(`
generate-ulart-image - UL Image Generation CLI

Generate Unsupervised Learning branded images using Flux 1.1 Pro, Nano Banana, or GPT-image-1.
Flux model uses Nano Banana (Gemini 3 Pro) via OpenRouter first, falls back to Flux 2 Pro if needed.

USAGE:
  generate-ulart-image --model <model> --prompt "<prompt>" [OPTIONS]

REQUIRED:
  --model <model>      Model to use: flux, nano-banana, nano-banana-pro, gpt-image-1
  --prompt <text>      Image generation prompt (quote if contains spaces)

OPTIONS:
  --size <size>              Image size/aspect ratio (default: 16:9)
                             Replicate (flux, nano-banana): 1:1, 16:9, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 21:9
                             OpenAI (gpt-image-1): 1024x1024, 1536x1024, 1024x1536
                             Gemini (nano-banana-pro): 1K, 2K, 4K (resolution); aspect ratio inferred from context or defaults to 16:9
  --aspect-ratio <ratio>     Aspect ratio for Gemini nano-banana-pro (default: 16:9)
                             Options: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
  --output <path>            Output file path (default: /tmp/ul-image.png)
  --reference-image <path>   Reference image for style/composition guidance (Nano Banana Pro only)
                             Accepts: PNG, JPEG, WebP images
                             Model will use this image as visual reference while following text prompt
  --transparent              Enable transparent background (adds transparency instructions to prompt)
                             Note: Not all models support transparency natively; may require post-processing
  --remove-bg                Remove background after generation using remove.bg API
                             Creates true transparency by removing the generated background
  --creative-variations <n>  Generate N variations (appends -v1, -v2, etc. to output filename)
                             Use with Kai's be-creative skill for true prompt diversity
                             CLI mode: generates N images with same prompt (tests model variability)
  --help, -h                 Show this help message

EXAMPLES:
  # Generate blog header with Nano Banana Pro (16:9, 2K quality)
  generate-ulart-image --model nano-banana-pro --prompt "Abstract UL illustration..." --size 2K --aspect-ratio 16:9

  # Generate high-res 4K image with Nano Banana Pro
  generate-ulart-image --model nano-banana-pro --prompt "Editorial cover..." --size 4K --aspect-ratio 3:2

  # Generate blog header with original Nano Banana (16:9)
  generate-ulart-image --model nano-banana --prompt "Abstract UL illustration..." --size 16:9

  # Generate square image with Flux
  generate-ulart-image --model flux --prompt "Minimal geometric art..." --size 1:1 --output /tmp/header.png

  # Generate portrait with GPT-image-1
  generate-ulart-image --model gpt-image-1 --prompt "Editorial cover..." --size 1024x1536

  # Generate 3 creative variations (for testing model variability)
  generate-ulart-image --model gpt-image-1 --prompt "..." --creative-variations 3 --output /tmp/essay.png
  # Outputs: /tmp/essay-v1.png, /tmp/essay-v2.png, /tmp/essay-v3.png

  # Generate with reference image for style guidance (Nano Banana Pro only)
  generate-ulart-image --model nano-banana-pro --prompt "Tokyo Night themed illustration..." \\
    --reference-image /tmp/style-reference.png --size 2K --aspect-ratio 16:9

NOTE: For true creative diversity with different prompts, use the creative workflow in Kai which
integrates the be-creative skill. CLI creative mode generates multiple images with the SAME prompt.

ENVIRONMENT VARIABLES:
  OPENROUTER_API_KEY      Primary for flux model (uses Nano Banana, fallback to Flux 2 Pro)
  OPENROUTER_BASE_URL     OpenRouter base URL (default: https://openrouter.ai/api/v1)
  REPLICATE_API_TOKEN     Required for nano-banana model (original Nano Banana on Replicate)
  OPENAI_API_KEY          Required for gpt-image-1 model
  GOOGLE_API_KEY          Required for nano-banana-pro model
  REMOVEBG_API_KEY        Required for --remove-bg flag

ERROR CODES:
  0  Success
  1  General error (invalid arguments, API error, file write error)

MORE INFO:
  Documentation: ~/.claude/skills/Art/README.md
  Source: ~/.claude/skills/Art/tools/generate-ulart-image.ts
`);
  process.exit(0);
}

// ============================================================================
// Argument Parsing
// ============================================================================

function parseArgs(argv: string[]): CLIArgs {
  const args = argv.slice(2);

  // Check for help flag
  if (args.includes("--help") || args.includes("-h") || args.length === 0) {
    showHelp();
  }

  const parsed: Partial<CLIArgs> = {
    model: DEFAULTS.model,
    size: DEFAULTS.size,
    output: DEFAULTS.output,
  };

  // Parse arguments
  for (let i = 0; i < args.length; i++) {
    const flag = args[i];

    if (!flag.startsWith("--")) {
      throw new CLIError(`Invalid flag: ${flag}. Flags must start with --`);
    }

    const key = flag.slice(2);

    // Handle boolean flags (no value)
    if (key === "transparent") {
      parsed.transparent = true;
      continue;
    }
    if (key === "remove-bg") {
      parsed.removeBg = true;
      continue;
    }

    // Handle flags with values
    const value = args[i + 1];
    if (!value || value.startsWith("--")) {
      throw new CLIError(`Missing value for flag: ${flag}`);
    }

    switch (key) {
      case "model":
        if (value !== "flux" && value !== "nano-banana" && value !== "nano-banana-pro" && value !== "gpt-image-1") {
          throw new CLIError(`Invalid model: ${value}. Must be: flux, nano-banana, nano-banana-pro, or gpt-image-1`);
        }
        parsed.model = value;
        i++; // Skip next arg (value)
        break;
      case "prompt":
        parsed.prompt = value;
        i++; // Skip next arg (value)
        break;
      case "size":
        parsed.size = value as Size;
        i++; // Skip next arg (value)
        break;
      case "aspect-ratio":
        parsed.aspectRatio = value as ReplicateSize;
        i++; // Skip next arg (value)
        break;
      case "output":
        parsed.output = value;
        i++; // Skip next arg (value)
        break;
      case "reference-image":
        parsed.referenceImage = value;
        i++; // Skip next arg (value)
        break;
      case "creative-variations":
        const variations = parseInt(value, 10);
        if (isNaN(variations) || variations < 1 || variations > 10) {
          throw new CLIError(`Invalid creative-variations: ${value}. Must be 1-10`);
        }
        parsed.creativeVariations = variations;
        i++; // Skip next arg (value)
        break;
      default:
        throw new CLIError(`Unknown flag: ${flag}`);
    }
  }

  // Validate required arguments
  if (!parsed.prompt) {
    throw new CLIError("Missing required argument: --prompt");
  }

  if (!parsed.model) {
    throw new CLIError("Missing required argument: --model");
  }

  // Validate reference-image is only used with nano-banana-pro
  if (parsed.referenceImage && parsed.model !== "nano-banana-pro") {
    throw new CLIError("--reference-image is only supported with --model nano-banana-pro");
  }

  // Validate size based on model
  if (parsed.model === "gpt-image-1") {
    if (!OPENAI_SIZES.includes(parsed.size as OpenAISize)) {
      throw new CLIError(`Invalid size for gpt-image-1: ${parsed.size}. Must be: ${OPENAI_SIZES.join(", ")}`);
    }
  } else if (parsed.model === "nano-banana-pro") {
    if (!GEMINI_SIZES.includes(parsed.size as GeminiSize)) {
      throw new CLIError(`Invalid size for nano-banana-pro: ${parsed.size}. Must be: ${GEMINI_SIZES.join(", ")}`);
    }
    // Validate aspect ratio if provided
    if (parsed.aspectRatio && !GEMINI_ASPECT_RATIOS.includes(parsed.aspectRatio)) {
      throw new CLIError(`Invalid aspect-ratio for nano-banana-pro: ${parsed.aspectRatio}. Must be: ${GEMINI_ASPECT_RATIOS.join(", ")}`);
    }
    // Default to 16:9 if not specified
    if (!parsed.aspectRatio) {
      parsed.aspectRatio = "16:9";
    }
  } else {
    if (!REPLICATE_SIZES.includes(parsed.size as ReplicateSize)) {
      throw new CLIError(`Invalid size for ${parsed.model}: ${parsed.size}. Must be: ${REPLICATE_SIZES.join(", ")}`);
    }
  }

  return parsed as CLIArgs;
}

// ============================================================================
// Prompt Enhancement
// ============================================================================

function enhancePromptForTransparency(prompt: string): string {
  const transparencyPrefix = "CRITICAL: Transparent background (PNG with alpha channel) - NO background color, pure transparency. Object floating in transparent space. ";
  return transparencyPrefix + prompt;
}

// ============================================================================
// Background Removal
// ============================================================================

async function removeBackground(imagePath: string): Promise<void> {
  const apiKey = process.env.REMOVEBG_API_KEY;
  if (!apiKey) {
    throw new CLIError("Missing environment variable: REMOVEBG_API_KEY");
  }

  console.log("🔲 Removing background with remove.bg API...");

  const imageBuffer = await readFile(imagePath);
  const formData = new FormData();
  formData.append("image_file", new Blob([imageBuffer]), "image.png");
  formData.append("size", "auto");

  const response = await fetch("https://api.remove.bg/v1.0/removebg", {
    method: "POST",
    headers: {
      "X-Api-Key": apiKey,
    },
    body: formData,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new CLIError(`remove.bg API error: ${response.status} - ${errorText}`);
  }

  const resultBuffer = Buffer.from(await response.arrayBuffer());
  await writeFile(imagePath, resultBuffer);
  console.log("✅ Background removed successfully");
}

// ============================================================================
// Image Generation
// ============================================================================

async function generateWithFlux(prompt: string, size: ReplicateSize, output: string): Promise<void> {
  // Try Nano Banana via OpenRouter FIRST (better with text in images)
  try {
    await generateWithNanoBananaOpenRouter(prompt, size, output);
    return;
  } catch (error) {
    console.log("⚠️  Nano Banana failed, trying Flux fallback...");
  }

  // Fallback to Flux via OpenRouter
  await generateWithFluxOpenRouter(prompt, size, output);
}

async function generateWithNanoBananaOpenRouter(prompt: string, size: ReplicateSize, output: string): Promise<void> {
  const apiKey = process.env.OPENROUTER_API_KEY;
  const baseURL = process.env.OPENROUTER_BASE_URL || 'https://openrouter.ai/api/v1';

  if (!apiKey) {
    throw new CLIError("Missing environment variable: OPENROUTER_API_KEY");
  }

  console.log("🍌 Generating with Nano Banana (google/gemini-3-pro-image-preview via OpenRouter)...");

  // Convert aspect ratio to approximate pixel dimensions for OpenRouter
  const dimensionsMap: Record<ReplicateSize, { width: number; height: number }> = {
    "1:1": { width: 1024, height: 1024 },
    "16:9": { width: 1920, height: 1080 },
    "9:16": { width: 1080, height: 1920 },
    "3:2": { width: 1536, height: 1024 },
    "2:3": { width: 1024, height: 1536 },
    "4:3": { width: 1408, height: 1056 },
    "3:4": { width: 1056, height: 1408 },
    "5:4": { width: 1280, height: 1024 },
    "4:5": { width: 1024, height: 1280 },
    "21:9": { width: 2560, height: 1080 },
  };

  const dimensions = dimensionsMap[size];

  const openai = new OpenAI({
    apiKey,
    baseURL
  });

  // OpenRouter uses chat completion API with modalities for image generation
  const response = await openai.chat.completions.create({
    model: "google/gemini-3-pro-image-preview",
    messages: [
      {
        role: "user",
        content: `Generate an image with dimensions ${dimensions.width}x${dimensions.height}: ${prompt}`
      }
    ],
    // @ts-ignore - OpenRouter extends OpenAI API with modalities
    modalities: ["image", "text"],
  });

  // Extract base64 image from response
  const message = response.choices[0]?.message;
  if (!message) {
    throw new CLIError("No message returned from OpenRouter API");
  }

  // OpenRouter returns images in a separate images array
  let imageData: string | undefined;

  // @ts-ignore - OpenRouter extends message with images array
  if (message.images && Array.isArray(message.images)) {
    // @ts-ignore
    const firstImage = message.images[0];
    if (firstImage?.image_url?.url) {
      const match = firstImage.image_url.url.match(/data:image\/\w+;base64,([^"]+)/);
      if (match) {
        imageData = match[1];
      }
    }
  }

  // Fallback: check content field
  if (!imageData && message.content) {
    if (typeof message.content === 'string') {
      const match = message.content.match(/data:image\/\w+;base64,([^"]+)/);
      if (match) {
        imageData = match[1];
      }
    } else if (Array.isArray(message.content)) {
      for (const part of message.content) {
        if (part.type === 'image_url' && part.image_url?.url) {
          const match = part.image_url.url.match(/data:image\/\w+;base64,([^"]+)/);
          if (match) {
            imageData = match[1];
            break;
          }
        }
      }
    }
  }

  if (!imageData) {
    throw new CLIError("No image data found in OpenRouter response");
  }

  const imageBuffer = Buffer.from(imageData, "base64");
  await writeFile(output, imageBuffer);
  console.log(`✅ Image saved to ${output}`);
}

async function generateWithFluxOpenRouter(prompt: string, size: ReplicateSize, output: string): Promise<void> {
  const apiKey = process.env.OPENROUTER_API_KEY;
  const baseURL = process.env.OPENROUTER_BASE_URL || 'https://openrouter.ai/api/v1';

  if (!apiKey) {
    throw new CLIError("Missing environment variable: OPENROUTER_API_KEY (fallback required)");
  }

  console.log("🎨 Generating with Flux 2 Pro (OpenRouter)...");

  // Convert aspect ratio to approximate pixel dimensions for OpenRouter
  const dimensionsMap: Record<ReplicateSize, { width: number; height: number }> = {
    "1:1": { width: 1024, height: 1024 },
    "16:9": { width: 1920, height: 1080 },
    "9:16": { width: 1080, height: 1920 },
    "3:2": { width: 1536, height: 1024 },
    "2:3": { width: 1024, height: 1536 },
    "4:3": { width: 1408, height: 1056 },
    "3:4": { width: 1056, height: 1408 },
    "5:4": { width: 1280, height: 1024 },
    "4:5": { width: 1024, height: 1280 },
    "21:9": { width: 2560, height: 1080 },
  };

  const dimensions = dimensionsMap[size];

  const openai = new OpenAI({
    apiKey,
    baseURL
  });

  // OpenRouter uses chat completion API with modalities for image generation
  const response = await openai.chat.completions.create({
    model: "black-forest-labs/flux.2-pro",
    messages: [
      {
        role: "user",
        content: `Generate an image with dimensions ${dimensions.width}x${dimensions.height}: ${prompt}`
      }
    ],
    // @ts-ignore - OpenRouter extends OpenAI API with modalities
    modalities: ["image", "text"],
  });

  // Extract base64 image from response
  const message = response.choices[0]?.message;
  if (!message) {
    throw new CLIError("No message returned from OpenRouter API");
  }

  // OpenRouter returns images in a separate images array
  let imageData: string | undefined;

  // @ts-ignore - OpenRouter extends message with images array
  if (message.images && Array.isArray(message.images)) {
    // @ts-ignore
    const firstImage = message.images[0];
    if (firstImage?.image_url?.url) {
      const match = firstImage.image_url.url.match(/data:image\/\w+;base64,([^"]+)/);
      if (match) {
        imageData = match[1];
      }
    }
  }

  // Fallback: check content field
  if (!imageData && message.content) {
    if (typeof message.content === 'string') {
      const match = message.content.match(/data:image\/\w+;base64,([^"]+)/);
      if (match) {
        imageData = match[1];
      }
    } else if (Array.isArray(message.content)) {
      for (const part of message.content) {
        if (part.type === 'image_url' && part.image_url?.url) {
          const match = part.image_url.url.match(/data:image\/\w+;base64,([^"]+)/);
          if (match) {
            imageData = match[1];
            break;
          }
        }
      }
    }
  }

  if (!imageData) {
    throw new CLIError("No image data found in OpenRouter response");
  }

  const imageBuffer = Buffer.from(imageData, "base64");
  await writeFile(output, imageBuffer);
  console.log(`✅ Image saved to ${output}`);
}

async function generateWithNanoBanana(prompt: string, size: ReplicateSize, output: string): Promise<void> {
  // Try Replicate first
  const token = process.env.REPLICATE_API_TOKEN;
  if (token) {
    try {
      const replicate = new Replicate({ auth: token });
      console.log("🍌 Generating with Nano Banana (Replicate)...");

      const result = await replicate.run("google/nano-banana", {
        input: {
          prompt,
          aspect_ratio: size,
          output_format: "png",
        },
      });

      await writeFile(output, result);
      console.log(`✅ Image saved to ${output}`);
      return;
    } catch (error) {
      console.log("⚠️  Replicate Nano Banana failed, trying OpenRouter fallback...");
    }
  } else {
    console.log("⚠️  No Replicate token, using OpenRouter fallback...");
  }

  // Fallback to OpenRouter with Gemini
  try {
    await generateWithNanoBananaOpenRouter(prompt, size, output);
    return;
  } catch (error) {
    console.log("⚠️  OpenRouter Gemini failed, trying Flux fallback...");
  }

  // Final fallback to Flux via OpenRouter
  await generateWithFluxOpenRouter(prompt, size, output);
}

async function generateWithGPTImage(prompt: string, size: OpenAISize, output: string): Promise<void> {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    throw new CLIError("Missing environment variable: OPENAI_API_KEY");
  }

  const openai = new OpenAI({ apiKey });

  console.log("🤖 Generating with GPT-image-1...");

  const response = await openai.images.generate({
    model: "gpt-image-1",
    prompt,
    size,
    n: 1,
  });

  const imageData = response.data[0].b64_json;
  if (!imageData) {
    throw new CLIError("No image data returned from OpenAI API");
  }

  const imageBuffer = Buffer.from(imageData, "base64");
  await writeFile(output, imageBuffer);
  console.log(`✅ Image saved to ${output}`);
}

async function generateWithNanoBananaPro(
  prompt: string,
  size: GeminiSize,
  aspectRatio: ReplicateSize,
  output: string,
  referenceImage?: string
): Promise<void> {
  const apiKey = process.env.GOOGLE_API_KEY;
  if (!apiKey) {
    throw new CLIError("Missing environment variable: GOOGLE_API_KEY");
  }

  const ai = new GoogleGenAI({ apiKey });

  if (referenceImage) {
    console.log(`🍌✨ Generating with Nano Banana Pro (Gemini 3 Pro) at ${size} ${aspectRatio} with reference image...`);
  } else {
    console.log(`🍌✨ Generating with Nano Banana Pro (Gemini 3 Pro) at ${size} ${aspectRatio}...`);
  }

  // Prepare content parts
  const parts: Array<{ text?: string; inlineData?: { mimeType: string; data: string } }> = [];

  // Add reference image if provided
  if (referenceImage) {
    // Read image file
    const imageBuffer = await readFile(referenceImage);
    const imageBase64 = imageBuffer.toString("base64");

    // Determine MIME type from extension
    const ext = extname(referenceImage).toLowerCase();
    let mimeType: string;
    switch (ext) {
      case ".png":
        mimeType = "image/png";
        break;
      case ".jpg":
      case ".jpeg":
        mimeType = "image/jpeg";
        break;
      case ".webp":
        mimeType = "image/webp";
        break;
      default:
        throw new CLIError(`Unsupported image format: ${ext}. Supported: .png, .jpg, .jpeg, .webp`);
    }

    parts.push({
      inlineData: {
        mimeType,
        data: imageBase64,
      },
    });
  }

  // Add text prompt
  parts.push({ text: prompt });

  const response = await ai.models.generateContent({
    model: "gemini-3-pro-image-preview",
    contents: [{ parts }],
    config: {
      responseModalities: ["TEXT", "IMAGE"],
      imageConfig: {
        aspectRatio: aspectRatio,
        imageSize: size,
      },
    },
  });

  // Extract image data from response
  let imageData: string | undefined;

  if (response.candidates && response.candidates.length > 0) {
    const parts = response.candidates[0].content.parts;
    for (const part of parts) {
      // Check if this part contains inline image data
      if (part.inlineData && part.inlineData.data) {
        imageData = part.inlineData.data;
        break;
      }
    }
  }

  if (!imageData) {
    throw new CLIError("No image data returned from Gemini API");
  }

  const imageBuffer = Buffer.from(imageData, "base64");
  await writeFile(output, imageBuffer);
  console.log(`✅ Image saved to ${output}`);
}

async function generateWithNanaBananaProWithFallback(
  prompt: string,
  size: GeminiSize,
  aspectRatio: ReplicateSize,
  output: string,
  referenceImage?: string
): Promise<void> {
  // Try Google Gemini API first
  try {
    await generateWithNanoBananaPro(prompt, size, aspectRatio, output, referenceImage);
    return;
  } catch (error) {
    console.log("⚠️  Gemini API failed, trying OpenRouter Nano Banana fallback...");
  }

  // Fallback to OpenRouter with Nano Banana (Gemini via OpenRouter)
  try {
    await generateWithNanoBananaOpenRouter(prompt, aspectRatio, output);
    return;
  } catch (error) {
    console.log("⚠️  OpenRouter Nano Banana failed, trying Flux fallback...");
  }

  // Final fallback to Flux via OpenRouter
  await generateWithFluxOpenRouter(prompt, aspectRatio, output);
}

// ============================================================================
// Main
// ============================================================================

async function main(): Promise<void> {
  try {
    // Load API keys from ${PAI_DIR}/.env
    await loadEnv();

    const args = parseArgs(process.argv);

    // Enhance prompt for transparency if requested
    const finalPrompt = args.transparent
      ? enhancePromptForTransparency(args.prompt)
      : args.prompt;

    if (args.transparent) {
      console.log("🔲 Transparent background mode enabled");
      console.log("💡 Note: Not all models support transparency natively; may require post-processing\n");
    }

    // Handle creative variations mode
    if (args.creativeVariations && args.creativeVariations > 1) {
      console.log(`🎨 Creative Mode: Generating ${args.creativeVariations} variations...`);
      console.log(`💡 Note: CLI mode uses same prompt for all variations (tests model variability)`);
      console.log(`   For true creative diversity, use the creative workflow in Kai with be-creative skill\n`);

      const basePath = args.output.replace(/\.png$/, "");
      const promises: Promise<void>[] = [];

      for (let i = 1; i <= args.creativeVariations; i++) {
        const varOutput = `${basePath}-v${i}.png`;
        console.log(`Variation ${i}/${args.creativeVariations}: ${varOutput}`);

        if (args.model === "flux") {
          promises.push(generateWithFlux(finalPrompt, args.size as ReplicateSize, varOutput));
        } else if (args.model === "nano-banana") {
          promises.push(generateWithNanoBanana(finalPrompt, args.size as ReplicateSize, varOutput));
        } else if (args.model === "nano-banana-pro") {
          promises.push(
            generateWithNanaBananaProWithFallback(
              finalPrompt,
              args.size as GeminiSize,
              args.aspectRatio!,
              varOutput,
              args.referenceImage
            )
          );
        } else if (args.model === "gpt-image-1") {
          promises.push(generateWithGPTImage(finalPrompt, args.size as OpenAISize, varOutput));
        }
      }

      await Promise.all(promises);
      console.log(`\n✅ Generated ${args.creativeVariations} variations`);
      return;
    }

    // Standard single image generation
    if (args.model === "flux") {
      await generateWithFlux(finalPrompt, args.size as ReplicateSize, args.output);
    } else if (args.model === "nano-banana") {
      await generateWithNanoBanana(finalPrompt, args.size as ReplicateSize, args.output);
    } else if (args.model === "nano-banana-pro") {
      await generateWithNanaBananaProWithFallback(
        finalPrompt,
        args.size as GeminiSize,
        args.aspectRatio!,
        args.output,
        args.referenceImage
      );
    } else if (args.model === "gpt-image-1") {
      await generateWithGPTImage(finalPrompt, args.size as OpenAISize, args.output);
    }

    // Remove background if requested
    if (args.removeBg) {
      await removeBackground(args.output);
    }
  } catch (error) {
    handleError(error);
  }
}

main();
