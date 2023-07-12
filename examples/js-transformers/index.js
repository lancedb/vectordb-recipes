// Copyright 2023 Lance Developers.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

'use strict'


const lancedb = require('vectordb')

async function example() {

    // Import transformers and the all-MiniLM-L6-v2 model (https://huggingface.co/Xenova/all-MiniLM-L6-v2)
    const { pipeline } = await import('@xenova/transformers')
    let pipe = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');


    // Create embedding function from pipeline
    const embed_fun = {}
    embed_fun.sourceColumn = 'text'
    embed_fun.embed = async function (batch) {
        let result = []
        for (let text of batch) {
            result.push((await pipe(text))['data'])
        }
        return result
    }


    // Link a folder and create a table with data
    const db = await lancedb.connect('data/sample-lancedb')

    const data = [
        { id: 1, text: 'Cherry', type: 'fruit'},
        { id: 2, text: 'Carrot', type: 'vegetable'},
        { id: 3, text: 'Cauliflower', type: 'vegetable'},
        { id: 4, text: 'Apple', type: 'fruit'},
        { id: 5, text: 'Banana', type: 'fruit'}
    ]

    const table = await db.createTable('food_table', data, "create", embed_fun)


    // Query the table
    const results = await table
        .search('something sweet to eat')
        .limit(2)
        .execute()
    console.log(results)

}

example().then(_ => { console.log("Done!") })
