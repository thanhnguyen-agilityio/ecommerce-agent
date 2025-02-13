Topic:
- [doc](https://docs.google.com/document/d/1z0VgEIQkmU3rv2gwrQMf0PMnjUCT7a2sak66sSNaORc/edit?tab=t.0#heading=h.lk913ur2m3ux)
- [project](https://github.com/users/thanhnguyen-agilityio/projects/2)


## Tasks

- [x] Clone practice 2 - LangChain advanced - Ivy moda agent
- [x] Context update - remove Ivy moda branding out of data, all data in english
  - Reason: this branding makes confusion more than helpful. Since the audience could ask why they need to data clone, why not use an online search tool directly.
  - Actions:
    - [x] 1. scrape ecommerce data with crawler (ref: Scrape from website instead of manual create ([Deepseek + Crawl4AI](https://www.youtube.com/watch?v=Osl4NgAXvRk)))
    - [x] 2. update documents related to remove branding
    - [x] 3. update product json with new data
- [ ] [HIGHEST] Flow update (v1)
  - Reason: apply human in the loop
  - Actions:
    - Separate tools
      - Safe tools: RAG, Search product in db
      - Sensitive tools: Search Google Shopping
    - Add human-in-the-loops for sensitive tools
     (Ref: [Build customer support chatbot](https://langchain-ai.github.io/langgraph/tutorials/customer-support/customer-support/) part 1,2,3)
- [ ] [HIGH] Flow update (v2)
  - Reason: add user info to graph, add more sensitive tools
  - Actions:
    - Update to use Supabase database
      - Setup Supabase database with products
      - Update code to use Supabase
    - Handle user authentication with Supabase
      - Add fetch user information node
      - Add tool to update user profile (sensitive tools)

This practice will build a customer support agent follow this diagram
![](https://langchain-ai.github.io/langgraph/tutorials/customer-support/img/part-3-diagram.png)


## Repositories:
- [Ecommerce Crawler](https://github.com/thanhnguyen-agilityio/ecommerce-crawler)
- [Ecommerce agent](https://github.com/thanhnguyen-agilityio/ecommerce-agent)
- [Fine-tuning LLM for ecommerce agent](https://github.com/thanhnguyen-agilityio/ecommerce-agent-fine-tuning)