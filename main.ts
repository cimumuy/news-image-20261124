// Hand-in copier for "The World in One Page: Tuesday 24 November 2026".
//
// The picture itself is drawn by compose.py, which writes entry.png next
// to this file. This program's only job is to deliver that file to the
// judging harness: it copies entry.png from the repository directory to
// /output/entry.png. Standard library only; runs under Deno or Node.

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const beside = join(here, "entry.png");
const source = existsSync(beside) ? beside : "./entry.png";
const target = "/output/entry.png";

mkdirSync("/output", { recursive: true });
copyFileSync(source, target);
console.log(`copied ${source} -> ${target}`);
