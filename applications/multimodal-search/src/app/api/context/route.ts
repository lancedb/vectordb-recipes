import { createEmbeddingsTable } from './insert'
import { NextResponse } from 'next/server'

export async function POST() {
  try {
    const name = await createEmbeddingsTable()
    return NextResponse.json({ table: name })
  } catch (e) {
    console.log(e)
    return NextResponse.json(e, {
      status: 400
    })
  }
}
