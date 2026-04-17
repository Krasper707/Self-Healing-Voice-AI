
# Initial Findings:

-[Link to paper](https://arxiv.org/html/2508.02296v1)
- Practitioners commonly attempt to mitigate OOD queries either by relying on the built-in guardrails of LLMs or by issuing additional LLM calls to explicitly judge whether a query is in-domain -> introduce significant overhead in terms of latency and API cost.
- Simple, low-dimensional representations can enable efficient, cost-effective, and interpretable OOD detection
[![](https://mermaid.ink/img/pako:eNpVkm1v0zAUhf_K1f1KVtq0adJoArVJVyZtCKaBNJJ98JKbxiOxK7-wja7_HedlICxZ8vV9zvGx5SMWsiSMsWrkU1EzZeA2zQW4sc6-aVLw1ZJ6uYezsw-wybbtA5Xj1kBt-k6SJbI9WEOQcm2YKAiMhKSx2jiLhIRRkpfaaQZV0qvS41_6HG5rRbqWTfnx9EalHfV6RxpeYZvdkFGcfhFUSrbwnQojFaQbGINse8uL7AvTGhIpDD0beDdk7cJcXV2P5EVP7rIdCVLMZV4L_URq7O767qfuOKsE3JA-SKHp_v9Qn6XLdOmgR5cD3sNa_3TXZYpXvGCGSzG6XQ5u6OFe8RLjijWaPGxJtayr8dhxOZqaWsoxdsuSKmYbk2MuTk53YOKHlC3GRlmnVNLu67fCHkqXP-Vsr9g_gkRJKpFWGIxnfu-A8RGfMQ78SRRG4WLpr-bRKohWHr5gHM4m_jxcTBdhFCz90I9OHv7uj5xOoiCIfDfDxXw6DZYzD6nk7uGvh1_Tf57THz8rsxM?type=png)](https://mermaid.live/edit#pako:eNpVkm1v0zAUhf_K1f1KVtq0adJoArVJVyZtCKaBNJJ98JKbxiOxK7-wja7_HedlICxZ8vV9zvGx5SMWsiSMsWrkU1EzZeA2zQW4sc6-aVLw1ZJ6uYezsw-wybbtA5Xj1kBt-k6SJbI9WEOQcm2YKAiMhKSx2jiLhIRRkpfaaQZV0qvS41_6HG5rRbqWTfnx9EalHfV6RxpeYZvdkFGcfhFUSrbwnQojFaQbGINse8uL7AvTGhIpDD0beDdk7cJcXV2P5EVP7rIdCVLMZV4L_URq7O767qfuOKsE3JA-SKHp_v9Qn6XLdOmgR5cD3sNa_3TXZYpXvGCGSzG6XQ5u6OFe8RLjijWaPGxJtayr8dhxOZqaWsoxdsuSKmYbk2MuTk53YOKHlC3GRlmnVNLu67fCHkqXP-Vsr9g_gkRJKpFWGIxnfu-A8RGfMQ78SRRG4WLpr-bRKohWHr5gHM4m_jxcTBdhFCz90I9OHv7uj5xOoiCIfDfDxXw6DZYzD6nk7uGvh1_Tf57THz8rsxM)

[![](https://mermaid.ink/img/pako:eNptksuS0zAQRX9F1Vs8wQ_FjryAim0WU5WpwBRssLPQRO3YlC2lJJkhZPLvKPY8AkQbqXVvdx89jrBVAiGFulOP24ZrS1b3lSRumOFhp_m-Ieu67lqJ5HPDDU7aeSyD8rYgXwbULZoNubn5QJZh-al_QCFaudtcOMNJjcq8G4x1CX_L0STTMkdptWqFIe_I10ajaVQnnp0oRSX_JZPXwLKg_GZQj2iHCSy7DpZNYFlUFq2xXG6RWEVeKS6dE2NGj-7MSpP1uvh4euEZDfRseLotnkg2L-_Rulv56SDyRqueF9llrflUKy5Xq7vL_XjaT8qlNI-oN1fqu76uwcI1-IFbS96TvOO6rQ__X9KSPp8NPNjpVkBa886gBz3qnp9jOJ6dFdgGe6wgdUuBNR86W0ElTy5vz-V3pXpIrR5cplbDrnkJhr3gFouWu6d4czgA1LkapIU08scKkB7hF6RhPEsCxljg04WbfT_24AApjWc-mzMasND3F4zRkwe_x57-jNFkkfhJOKdRyJzmAYrWKn03fdnx557-ABjCzI4?type=png)](https://mermaid.live/edit#pako:eNptksuS0zAQRX9F1Vs8wQ_FjryAim0WU5WpwBRssLPQRO3YlC2lJJkhZPLvKPY8AkQbqXVvdx89jrBVAiGFulOP24ZrS1b3lSRumOFhp_m-Ieu67lqJ5HPDDU7aeSyD8rYgXwbULZoNubn5QJZh-al_QCFaudtcOMNJjcq8G4x1CX_L0STTMkdptWqFIe_I10ajaVQnnp0oRSX_JZPXwLKg_GZQj2iHCSy7DpZNYFlUFq2xXG6RWEVeKS6dE2NGj-7MSpP1uvh4euEZDfRseLotnkg2L-_Rulv56SDyRqueF9llrflUKy5Xq7vL_XjaT8qlNI-oN1fqu76uwcI1-IFbS96TvOO6rQ__X9KSPp8NPNjpVkBa886gBz3qnp9jOJ6dFdgGe6wgdUuBNR86W0ElTy5vz-V3pXpIrR5cplbDrnkJhr3gFouWu6d4czgA1LkapIU08scKkB7hF6RhPEsCxljg04WbfT_24AApjWc-mzMasND3F4zRkwe_x57-jNFkkfhJOKdRyJzmAYrWKn03fdnx557-ABjCzI4)


## Multi Agent System?

- 1. **Retrieval Agents**: Optimize document retrieval using multiple retrievers (e.g., hybrid sparse-dense search).
- 2. Validation Agents: Assess retrieved documents' relevance, reliability, and recency.

- 3. Reasoning Agents: Apply multi-step reasoning (e.g., OpenAI o1/o3) to synthesize retrieved information.
- 4. Generation Agents: Formulate responses using context-aware generation models


## Centroid ahh checking
- When the user asks for "donut coupons", you retrieve the Top-K chunks. 
- Then Calculate the entropy of the cosine similarity scores of those chunks.
- Low Entropy / Sharp Peak: One or two chunks have a very high similarity score (e.g., 0.85+). The answer is in the KB.
- High Entropy / Flat Distribution: All Top-K chunks have mediocre, similar scores (e.g., 0.40 to 0.45). This means the Vector DB is "guessing" because the actual knowledge is missing.


- If the max similarity is below a threshold θ AND the entropy is high, we have detected the "Delta".



Log EVERYTHING that triggers the "Delta". If the user asks for gold bars, a PS5, or "how far is the moon", and the Vector DB doesn't know the answer, it triggers the Delta logic. Log it all to the asynchronous queue.


Move the "Noise Filtering" offline. Have a daily CRON job or batch process that uses a heavier, smarter LLM to cluster the Deltas. The offline LLM will easily recognize that "how far is the moon" is garbage, but "gold bars" and "donut coupons" are massive missed business opportunities.

The Voice Response: If a Delta is detected, the bot simply gives a polite fallback: "I don't have information on that right now, but I've noted your request for our team!"

## Handling 
### Option A: Live Retrieval (External Sources)
- Web search
- APIs
- DBs
  

### Option B: Query expansion  
- Send the query to an LLM to  elaborate / expand the query i.e. if the  user asks for "What is GPT-5 architecture?" ; Give  ["GPT-5 model architecture details","latest OpenAI model design",
"transformer improvements post GPT-4"]

### Option C (Not as significant as others but could work I suppose)
- Before searching the Vector DB, a very fast model (or zero-shot classifier) determines the Domain. If the user asks about "Cars" on a "Donut" app, it gets blocked instantly.



## PCA (subspace in the vector space)
- Project query embeddings into an in-domain subspace learned from KB documents. `Triantafyllopoulos et al. (2024/25)` compute principal components (PCA) of the document embedding space and project new queries into this low-dimensional subspace
- Queries that lie far outside the ID distribution (e.g. as measured by explained-variance ratio or by a statistical test on PCA components) are flagged as OOD. A Gaussian Mixture Model (GMM) or Mahalanobis distance can be used in this reduced space to classify in- vs. out-of-domain

## LLM As A Judge:
- One may prompt the LLM (or a separate language model) to judge whether the retrieved context supports the query
- But this could take up more time than necessary(due to API Calls)




# Metrics to check effectiveness for
### Context Overlap / Recall: 
 - Intuitively, if the answer contains ideas or terms not found in the retrieved documents, there is a gap 
### Answer Relevancy (Intent Alignment): 
- Even if context is adequate, the system should detect when its generated answer drifts off-topic. Answer Relevancy measures how well the final answer addresses the original query


# Expansion of Knowledge Base
- Query Log : Track user queries and their outcomes to find systemic gaps. For any query where retrieval fails or confidence is low, log the query and its features for offline analysis. As one RAG guide notes: if a query returns “no relevant information”, the system should log it for knowledge gap analysis
- Continuous Retrieval: If internal retrieval is flagged as incorrect, CRAG(Corrective RAG) “triggers a web search to pull in fresher or supplemental information” to fill the gap


[![](https://mermaid.ink/img/pako:eNpNkmtv2jAUhv-K5Q9TJgEN5epU2sS9FLq2bNW0AR_c5ASsOXbqCy1D_Pc6Doh-ii_Pef2eN-eAY5kAjvBG0XyL5ouVQKi3fNag0JMFtV-javUb6gdTYUAYdIUeFeRKxqA1E5uvNwXf98wgWIBRDHaABtLR76a8Hfjb4WGqz-doARx21MlRkaBeAq-WGvh-9PjQ4eiH9EWjwHtwfCpVZjk1TArn4Te8oDHl_IXG_8pHRqWFi8If0P5oHExAgHL6qCf0m2trxyiaz-_LurGHJsFoR7n9BD1ZypnZl9DEQ7eH092YMrNNLUdf0IOo_pI5i0_ebz95nwY_gafVWCoFceE7QgpSJgDFpxSkQi7JLD_lNC39XoTOLdwVwVolzt7erlDMjM9Cl6V3npst53JT_rXCmjWxzECvPTHzxHz5kKa88NATlO810y7MWR8954nrfX2DK24OWIKjlHINFZyBymixx4dCZIXNFjJY4cgtE0ip5WaFV-Lo6nIq_kqZ4cgo6yqVtJvteWO9_JBRN2QXAkQCaiCtMDgiXgBHB_yOo-t2rVMnhNTDZtd9w7BdwXscNdu1kLRIs06uw7BLSPNYwf_9k2GNNDvdTthp1ButRqdFuhUMCTNS3ZfD7Wf8-AGVf-Z8?type=png)](https://mermaid.live/edit#pako:eNpNkmtv2jAUhv-K5Q9TJgEN5epU2sS9FLq2bNW0AR_c5ASsOXbqCy1D_Pc6Doh-ii_Pef2eN-eAY5kAjvBG0XyL5ouVQKi3fNag0JMFtV-javUb6gdTYUAYdIUeFeRKxqA1E5uvNwXf98wgWIBRDHaABtLR76a8Hfjb4WGqz-doARx21MlRkaBeAq-WGvh-9PjQ4eiH9EWjwHtwfCpVZjk1TArn4Te8oDHl_IXG_8pHRqWFi8If0P5oHExAgHL6qCf0m2trxyiaz-_LurGHJsFoR7n9BD1ZypnZl9DEQ7eH092YMrNNLUdf0IOo_pI5i0_ebz95nwY_gafVWCoFceE7QgpSJgDFpxSkQi7JLD_lNC39XoTOLdwVwVolzt7erlDMjM9Cl6V3npst53JT_rXCmjWxzECvPTHzxHz5kKa88NATlO810y7MWR8954nrfX2DK24OWIKjlHINFZyBymixx4dCZIXNFjJY4cgtE0ip5WaFV-Lo6nIq_kqZ4cgo6yqVtJvteWO9_JBRN2QXAkQCaiCtMDgiXgBHB_yOo-t2rVMnhNTDZtd9w7BdwXscNdu1kLRIs06uw7BLSPNYwf_9k2GNNDvdTthp1ButRqdFuhUMCTNS3ZfD7Wf8-AGVf-Z8)


# Evaluation 
- RAG Benchmarks: Standard QA datasets (Natural Questions, TriviaQA, WebQuestions) and specialized RAG benchmarks (KILT tasks such as WNED-Wikipedia, FEVER fact-checking, HoVer for reference-based QA)
- RAGAS



## Human in the loop RAG :
- When performing update, show human, if human finds it unncessary, make appropriate changes / do not add it tot he knowledge base

**