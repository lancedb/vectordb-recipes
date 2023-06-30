(async () => {
  const lancedb = require('vectordb')
  const db = await lancedb.connect("data/sample-lancedb")
  db.openTable("hi")
})();