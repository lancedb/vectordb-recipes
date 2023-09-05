import { connect } from "vectordb";

import sharp from "sharp";
import * as path from "path";
import * as fs from "fs";

async function processImgs(imgs_dir: string, db: any) {
  const imgs = fs.readdirSync(path.join(process.cwd(), imgs_dir));
  var img_files = [];
  for (var i = 0; i < imgs.length; i++) {
    img_files.push(
      (
        await sharp(path.join(process.cwd(), imgs_dir, imgs[i]))
          .resize(200, 200)
          .jpeg({ quality: 50 })
          .toBuffer()
      ).toString("base64")
    );
  }
  const baseUrl = process.env.VERCEL_URL
    ? "https://" + process.env.VERCEL_URL
    : "http://localhost:3000";
  var embeddings = [];

  for (var i = 0; i < img_files.length; i++) {
    console.log("Getting embeddings for image " + i);
    const response = await fetch(`${baseUrl}/api/embed`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ data: img_files[i], type: "image" }),
    });
    const json = await response.json();
    embeddings.push(json.embedding);
  }

  var data = [];
  for (var i = 0; i < img_files.length; i++) {
    data.push({
      img: path.join("/", "coco128/images/train2017", imgs[i]), // Hardcoded but I don't even care at this point
      vector: embeddings[i],
    });
  }
  await db.createTable(process.env.LANCEDB_TABLE_NAME, (data = data));

  return process.env.LANCEDB_TABLE_NAME;
}

export async function createEmbeddingsTable() {
  const { promisify } = require("util");
  const exec = promisify(require("child_process").exec);

  const LANCEDB_URI: string = process.env.LANCEDB_URI || "table";
  const LANCEDB_TABLE_NAME: string = process.env.LANCEDB_TABLE_NAME || "table";
  const db = await connect(LANCEDB_URI);
  const tableNames = await db.tableNames();
  console.log("table names ", tableNames);
  if (tableNames.includes(LANCEDB_TABLE_NAME)) return LANCEDB_TABLE_NAME;

  // Exec output contains both stderr and stdout outputs
  console.log("Downloading COCO128 dataset");
  await exec(
    "wget https://ultralytics.com/assets/coco128.zip -O public/coco128.zip"
  );
  console.log("Unzipping COCO128 dataset");
  await exec("unzip -o public/coco128.zip -d public/");
  console.log(" unzipped");

  const imgs_dir = "public/coco128/images/train2017";

  return await processImgs(imgs_dir, db);
}
