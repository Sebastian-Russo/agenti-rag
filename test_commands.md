$ python app.py

$ curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Compare how Dumbledore and Snape viewed Harry role in defeating Voldemort"}'

(venv) sebastian~/ai-projects/agenti-rag(main) $ curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Compare how Dumbledore and Snape viewed Harry role in defeating Voldemort"}'
{
  "answer": "# Dumbledore and Snape's Views on Harry's Role in Defeating Voldemort\n\n## Dumbledore's Perspective\n\nDumbledore held a nuanced and deeply considered view of Harry's role in defeating Voldemort. While he acknowledged the prophecy's importance \u2014 that a boy born to parents who had defied Voldemort could rise up and defeat him \u2014 he was careful not to reduce Harry to merely a instrument of fate. In fact, Dumbledore actively pushed back against Harry placing too much weight on the prophecy itself, telling him pointedly, \"You are setting too much store by the prophecy!\"\n\nDumbledore's central argument was that Harry's role was ultimately a matter of personal choice and character, not just destiny. He challenged Harry to imagine he had never heard the prophecy and asked how he would feel about Voldemort then \u2014 pointing to Harry's personal losses (his parents, Sirius, Cedric) as the true motivation. Most tellingly, Dumbledore explained that it was Voldemort himself who had made Harry \"the person who would be most dangerous to him\" by singling him out. He emphasized that Harry was \"quite free to turn your back on the prophecy,\" but that Voldemort's continued belief in it made a final confrontation inevitable. The evidence suggests Dumbledore wanted Harry to walk into that confrontation with agency and dignity \u2014 the difference, as Harry came to understand, between \"being dragged into the arena\" and \"walking into the arena with your head held high.\"\n\n## Snape's Perspective\n\nThe retrieved evidence provides a less direct window into Snape's own explicit views on Harry's role in defeating Voldemort. What the passages do reveal is that Snape's relationship with Harry was complex and often antagonistic on the surface. Snape functioned as a constant abrasive force in Harry's life \u2014 tormenting him in Potions and later in Defense Against the Dark Arts \u2014 though some interpretations suggest this pressure helped mold Harry into who he needed to become.\n\nCrucially, Snape operated under Dumbledore's orders throughout much of the series, including his role as a spy against Voldemort \"at great personal risk.\" His actions, such as killing Dumbledore at Dumbledore's own request to protect Draco Malfoy and maintain his cover, suggest he was working toward the ultimate goal of Voldemort's defeat. However, his motivation appears to have been driven primarily by his love for Lily Potter rather than any overt belief in Harry as a chosen hero.\n\n## Comparison\n\nUltimately, Dumbledore viewed Harry's role as rooted in both prophecy and personal moral agency, carefully guiding Harry to embrace his destiny as a free choice rather than an obligation. Snape's view, based on the available evidence, is harder to define explicitly \u2014 his actions supported Harry's survival and Voldemort's defeat, but seemingly more out of loyalty to Dumbledore and love for Lily than out of a philosophically formed belief in Harry's heroic destiny. Where Dumbledore elevated and empowered Harry, Snape's role was more covert and, outwardly at least, appeared adversarial.",
  "question": "Compare how Dumbledore and Snape viewed Harry role in defeating Voldemort",
  "retrieval_quality": 6.0,
  "sub_queries": [
    "Dumbledore Harry role defeating Voldemort prophecy",
    "Snape Harry role defeating Voldemort",
    "Dumbledore Snape disagreement Harry",
    "Snape protection Harry Dumbledore orders"
  ],
  "sub_query_summaries": [
    {
      "attempts": 1,
      "chunks_used": 5,
      "score": 6,
      "sub_query": "Dumbledore Harry role defeating Voldemort prophecy",
      "succeeded": true
    },
    {
      "attempts": 1,
      "chunks_used": 5,
      "score": 6,
      "sub_query": "Snape Harry role defeating Voldemort",
      "succeeded": true
    },
    {
      "attempts": 1,
      "chunks_used": 5,
      "score": 6,
      "sub_query": "Dumbledore Snape disagreement Harry",
      "succeeded": true
    },
    {
      "attempts": 1,
      "chunks_used": 5,
      "score": 6,
      "sub_query": "Snape protection Harry Dumbledore orders",
      "succeeded": true
    }
  ],
  "total_chunks_used": 20
}
(venv) sebastian~/ai-projects/agenti-rag(main) $
