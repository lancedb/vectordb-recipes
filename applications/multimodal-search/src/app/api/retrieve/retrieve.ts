import { connect } from "vectordb";

export async function retrieveContext(query: Array<number>, table: string) {
  const db = await connect(process.env.LANCEDB_URI || "database");
  const tbl = await db.openTable(table);

  const result = await tbl.search(query).select(["img"]).limit(25).execute();

  const imgs = result.map((r: any) => r.img);

  return imgs;
}
