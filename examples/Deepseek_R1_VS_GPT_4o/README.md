# DeepSeek R1 vs GPT-4o: Which AI Model Excels in RAG?

## Introduction
DeepSeek R1 and GPT-4o are emerging as powerhouses in the AI world, competing in real-world business applications. This comparison covers key factors like **cost, architecture, and RAG performance** to determine which model excels in different scenarios. Is DeepSeek R1's cost advantage enough to challenge GPT-4o's speed and multimodal capabilities?

### Experiment Setup  

We conducted an evaluation of two models using a **Zomato case study** with **RAG-based retrieval** to compare the reasoning capabilities of a **thinking model** versus a **chat model**.  

### Configuration  

- **Model Used**: DeepSeek R1 (1.5B) running locally via **Ollama** (Note: This is not the full **671B MoE model**, which outperforms GPT-4o in accuracy).  
- **Inference Setup**:  
  - Running **DeepSeek R1 (1.5B)** locally using [Ollama](https://ollama.com/library/deepseek-r1:1.5b).  
  - You can experiment with larger models if desired.  
  - To run the model locally:  
    ```bash
    ollama run deepseek-r1:1.5b
    ```  
  - Start the application:  
    ```bash
    python app.py
    ```  
- **Further Experimentation**: Optionally, you can use the **DeepSeek API** for extended testing.  


## Comparative Analysis

### Query 1: Commission Structure Analysis
**Question:** How does Zomato's commission structure compare with global food delivery players like Grubhub and Meituan, and what implications does this have for its future market positioning?

#### DeepSeek R1 Response:
```
###  DeepSeek R1 Response ### :
<think>
Okay, so I'm trying to figure out how Zomato's commission structure compares to other big food delivery companies like Grubhub and Meituan. From what the user wrote, they mentioned that in a previous conversation, the human asked about the comparison, and the bot said there wasn't much information available yet.
First, I need to understand what a commission structure means. It's how much of the money you earn from each delivery. The higher it is, the better for the restaurant because more profit. So Zomato wants to know if their commission rate is better than Grubhub and Meituan.
Looking at Deliveroo's financials: They had total transaction volume around £41 billion in 2020, which includes on-demand food delivery. Their gross transaction value (GTV) grew by 64% over the past two years. GTV is like the value of all transactions, so if they have more GTV, that's better. They mentioned 51.3% from the UK and Ireland, and 48.7% from others. That suggests a high demand there, but maybe it's not the only factor.
Deliveroo's commission per order decreased slightly over the years because delivery cost as a percentage of GMV increased. So while GTV went up, if delivery costs took away more relative to total sales, their per-order commission goes down.
Looking at Meituan and Grubhub, they are large players with higher GTVs but I don't have exact commission rates. From Deliveroo's 2019 data, the restaurant's commission was around 8%, which is higher than what Meituan or Grubhub might have if their GTV was significantly larger.
Zomato's commission structure seems different because it might be more about on-demand delivery rather than full restaurants. They started a new service called "Order Direct" with the app, which they plan to launch in August 2021. This app would allow restaurants to get more direct deliveries without relying solely on Grubhub or Meituan.
Zomato's commission structure is designed for their specific needs -- on-demand food delivery, so it might be structured differently from other companies that handle all types of restaurant orders. They have a model where they focus on delivering small batches quickly to nearby restaurants. This could potentially set them apart in terms of revenue streams and customer acquisition strategies.
In contrast, Grubhub and Meituan deliver more across a wider range of locations and include all kinds of food items. Their commission structures might be more about covering these broader areas, which could mean lower per-order rates because the volume is higher and they have to cover more types of orders.
So, putting it together: Zomato's commission structure is tailored for their on-demand delivery model, focusing on delivering small batches quickly. This approach might allow them to keep a higher commission rate compared to Grubhub and Meituan, which handle more varied orders across different regions.
However, the user also mentioned that in Deliveroo's financials, their GTV growth came with a 64% increase, but the commission structure didn't show much comparison. So while Zomato has high demand in certain areas, their main focus is on faster delivery rather than a broader market.
Another point from Deliveroo is that they saw increased reliance on food delivery operators (duopoly) which led to restaurants trying to launch Order Direct. This aligns with Zomato's approach of having a separate app or platform dedicated to their specific needs.
So, in summary, Zomato's commission structure is aimed at their unique need for on-demand small batch deliveries, allowing them to manage their revenue and customer acquisition through this model.
</think>


Zomato's commission structure is tailored for its unique need for delivering on-demand food items quickly, targeting restaurants that can accept these deliveries. This model allows Zomato to manage its revenue and customer acquisition by focusing solely on delivering small batches of food within a limited timeframe, which is a key differentiator compared to other companies like Grubhub or Meituan.
Zomato's approach emphasizes fast delivery for specific locations, which reduces the volume of orders that cover broader areas. In contrast, these larger companies deliver across more regions and include a wider variety of food items, potentially leading to higher commission rates due to increased GTV (total transaction value).
Additionally, Zomato has introduced an "Order Direct" app aimed at restaurants seeking quick access to on-demand delivery services. This feature could differentiate Zomato from competitors that focus on full-service restaurant operations.
Overall, while Zomato's commission structure may not be directly comparable to the financial metrics of Grubhub or Meituan as revealed in Deliveroo's data, its specific needs for on-demand delivery and its unique platform approach set it apart.
```

#### OpenAI Response:
```
Zomato's commission structure is tailored for its unique need for delivering on-demand food items quickly, targeting restaurants that can accept these deliveries. This model allows Zomato to manage its revenue and customer acquisition by focusing solely on delivering small batches of food within a limited timeframe, which is a key differentiator compared to other companies like Grubhub or Meituan.
Zomato's approach emphasizes fast delivery for specific locations, which reduces the volume of orders that cover broader areas. In contrast, these larger companies deliver across more regions and include a wider variety of food items, potentially leading to higher commission rates due to increased GTV (total transaction value).
Additionally, Zomato has introduced an "Order Direct" app aimed at restaurants seeking quick access to on-demand delivery services. This feature could differentiate Zomato from competitors that focus on full-service restaurant operations.
Overall, while Zomato's commission structure may not be directly comparable to the financial metrics of Grubhub or Meituan as revealed in Deliveroo's data, its specific needs for on-demand delivery and its unique platform approach set it apart.
```

### Query 2: Zomato Pro+ Impact Analysis
**Question:** How is the introduction of Zomato Pro+ expected to impact customer retention, revenue, and profitability over the next five years?

#### DeepSeek R1 Response:
```
<think>
Alright, let me try to work through this query. The user has provided a series of documents about Zomato's delivery business model, including some financial data and contact information. They also mentioned previous conversations where they asked about how the introduction of Zomato Pro+ would impact retention, revenue, and profitability over five years.
First, I need to understand the context. The main documents are PDFs discussing Zomato's delivery costs and customer incentives. There are several sections with different data points: employee cost percentages, delivery costs, incentives, government breakpoints for the food delivery business, and company contact info.
The user's question is about how introducing Zomato Pro+ would affect retention, revenue, and profitability over five years. So, I need to extract relevant information from the provided PDFs that relate to product differentiation, customer acquisition strategies, or any changes in operations that could impact these areas.
Looking at the financial data, there's a section discussing employee cost percentages (37% in FY21 to 16.5% in FY30E). This suggests that Zomato Pro+ might offer better pay, which could help retain employees and possibly increase retention rates as they receive higher compensation.
There are also mentions of different delivery models, including the 'Service rendered at a point in time' model where revenue comes from commission-based sales plus transaction fees. This could imply that offering more value or a better deal (via Pro+) might attract existing customers and help with acquisition strategies.
The government breakup section shows how costs like food discounts and other variable costs are structured, which is important for understanding cost-saving measures. If Zomato Pro+ introduces new features or pricing models, the impact on these cost structures could affect profitability in the long run.
Additionally, there's a contact information section with specific phone numbers and emails, which might be relevant if Zomato Pro+ involves any changes in their business operations that would require updates to their workforce or marketing strategies. However, without more details on how exactly Pro+ is implemented, it's challenging to assess its impact directly.
Putting this together, the key points are:
- Higher employee cost percentage (from 37% to 16.5%) might indicate better compensation for existing employees.
- Potential increase in customer acquisition through a better value proposition or new features offered by Pro+.
- Impact on profitability from reduced costs due to more aggressive pricing or lower discounts.
I should structure my response to address each of these points, providing specific data and possible explanations based on the provided documents. This way, the user gets a clear understanding of how Zomato Pro+ could affect their business in the next five years.
</think>

Based on the provided documents and conversations, here are some insights that can help you understand how the introduction of **Zomato Pro** might impact customer retention, revenue, and profitability over the next five years:

### 1. **Impact on Employee Retention**
From the financial data, it appears that Zomato Pro+ could potentially reduce the percentage of employees who are paid based on their work performance (e.g., higher compensation rates) due to its improved pricing or value propositions. This could lead to:
**Higher employee retention** as customers perceive better pay.
Increased demand for in-house training and development programs if the company introduces a new product or service.

### 2. **Potential Increase in Customer Acquisition**
Zomato Pro+ might introduce new features, pricing models, or value additions that attract existing customers:
Improved delivery reliability or speed.
More competitive pricing for their services.
Enhanced customer support or loyalty programs.
This could lead to increased **customer acquisition costs (CAC)** if the company introduces new offerings but faces higher competition.

### 3. **Impact on Profitability**
The financial breakdowns mention "food discounts" and other variable costs, which are deducted from total delivery costs. If Zomato Pro+ introduces more efficient or cost-effective ways to deliver food (e.g., better packaging, faster service), it could:
Reduce overall **delivery costs**.
Lower the percentage of revenue spent on **variable costs**.
These changes could improve profitability over the next five years.

### 4. **Government Breakdown and Cost Structures**
The government breakpoints mentioned in the financial data likely outline how Zomato Pro+ might affect their food delivery business:
Stronger restrictions on cost-cutting measures for food delivery businesses.
More emphasis on transparency and accountability in pricing and delivery performance.
This could lead to **higher costs** or stricter compliance with regulations if the company introduces new product lines or pricing strategies.

### 5. **Customer Acquisition Signals**
If Zomato Pro+ introduces a new feature (e.g., loyalty program, personalized recommendations) that enhances customer experience and builds brand awareness, it could:
Increase customer retention.
Lower acquisition costs by reducing transaction fees or promoting in-store experiences.
This would support long-term profitability.

### 6. **Human Resources and Workforce Changes**
If Zomato Pro+ involves changes to the company's structure (e.g., more roles, new teams), it could:
Increase employee engagement as employees see higher compensation or better benefits.
Require changes in workforce policies or training to support new initiatives.

### 7. **Market Competition**
Zomato Pro+ might introduce a competitive product line or service that:
Attracts existing customers with better pricing or features.
Creates demand for the company's current offerings if they align with similar products.

### Summary
The introduction of **Zomato Pro** could have several positive impacts on your business over the next five years, including:
Better employee retention due to improved compensation structures.
Potential increases in customer acquisition costs or demand for new services.
Improved profitability from cost-cutting measures and higher pricing strategies.
To gain more concrete insights, I recommend reviewing any press releases, product launches, or official statements related to Zomato Pro+ with your team.
```

#### GPT-4o Response:
```
The introduction of Zomato Pro+ is expected to have several impacts on customer retention, revenue, and profitability over the next five years:
1. **Customer Retention**: Zomato Pro+ offers customers the advantage of free unlimited deliveries, which is likely to appeal to existing power users and potentially increase customer retention. The subscription model encourages users to order more frequently to maximize the value of their membership, thereby increasing engagement with the platform.
2. **Revenue**: While the Pro+ program may initially boost revenue through subscription fees, it could also lead to a decrease in per-order revenue. This is because Pro+ users will not pay delivery fees, which are a significant component of Zomato's revenue. Additionally, the program might shift the burden of discounts more towards restaurants, potentially affecting Zomato's revenue from restaurant commissions.
3. **Profitability**: In the short term, the Pro+ program is expected to dent profitability due to increased delivery costs, as deliveries to Pro+ customers will be free. This will prolong the need for delivery-cost subsidies. However, over the long term, the program could help reduce discount costs as the burden shifts to restaurants. Zomato's management has indicated a focus on long-term growth over short-term profitability, suggesting that significant improvements in profitability might not be expected until FY26 or later.
Overall, while Zomato Pro+ may enhance customer retention and engagement, its impact on revenue and profitability is complex, with potential short-term challenges but possible long-term benefits as the company focuses on growth and market expansion.
```

### Query 3: Investment Strategy Analysis
**Question:** Given Zomato's revenue growth projections, cost structure, and competitive environment, would an investor be better off holding, selling, or increasing their stake in Zomato?

#### DeepSeek R1 Response:
```
Okay, let me try to figure this out. So, the user provided a lot of financial information about three companies: GrubHub, Deliveroo, and Delivery Hero. They also asked a question about whether an investor would hold onto, sell, or increase their stake in Zomato based on revenue growth projections and cost structure.
First, I need to understand each company's financial data. Grubhub had a Market Gross Order Value of $24.5 billion and Contribution Profit of $663 million for the year ending December 31, 2020. That's pretty significant, but they lost half their value in three years and ended up with negative net profits after adjusting for losses during FY19 and FY20.
Deliveroo had a growth in Gross Transaction Value to £4.1 billion from £2.5 billion, which is a 64% increase. They also added more revenue streams like on-demand delivery and partnerships, contributing to their profitability.
Delivery Hero had operating income growing by about $39% of GMV since FY17 to 64%, but their contribution per order dropped because delivery costs went up faster than they earned from each order. This could be a red flag if the business is becoming more expensive.
Now, Zomato isn't mentioned here, so I'm not sure how that ties in. The user asked about an investor's decision based on these factors. They might be worried about whether their investment would dilute or become undervalued as the company grows.
I should consider trends. Grubhub and Deliveroo are expanding into new markets, which can boost revenue but may also increase costs if logistics get more complex. Delivery Hero seems to have diversified operations, possibly offsetting some growth with higher costs in their services like kitchens or Dmarts.
The user's question is about investor decisions. They might be concerned that Zomato could become less profitable as it grows, leading to dilution. Alternatively, they might be worried about the company becoming overpriced if it continues growing without improving margins or reducing costs.
I should probably suggest factors like expansion into new markets vs cost management, diversification strategies, and profitability trends. Maybe also mention that investors need to look at cash flow, risk tolerance, and whether there are alternatives with similar growth potential but lower risks.
```

#### GPT-4o Response:
```
Based on the provided content, Zomato is projected to experience significant revenue growth, with an expected Revenue CAGR of 33% over FY21-FY30E. However, the company is currently facing challenges related to profitability due to its strategy of subsidizing customers, delivery partners, and restaurant partners to drive growth. This approach results in a continued cash burn, which is expected to persist for the next few years.
The competitive environment is intense, with existing players like Swiggy and potential new entrants posing significant threats. Additionally, Zomato's expansion into new cities and customer acquisition efforts require substantial investment, further impacting profitability.
The report initiates coverage with a "Sell" rating and a target price of Rs 90 per share, suggesting a downside from the current market price. This implies that the market anticipates a longer gestation period before Zomato can achieve profitability, and the steep revenue multiples may degrade faster than the growth rate moderates.
Given these factors, the recommendation is to sell, as the risks associated with profitability, competition, and sustained cash burn outweigh the potential benefits of holding or increasing the stake in Zomato at this time.
```

### Query 4: Revenue Stream Analysis
**Question:** What are the three main ways Zomato earns revenue?

#### DeepSeek R1 Response:
```
Okay, so I need to figure out how Zomato's current revenue sources work. From the provided information, there are several parts about their operations and their financial details.
First, looking at the company structure and financial data: Zomato has multiple subsidiaries with different percentages invested in India, Middle East, Asia-Pacific, etc. Each subsidiary is allocated a certain percentage of Rs 50 billion. This shows they're spread out geographically but have significant investments in key markets like India where they target their delivery service.
The financial statements mention that as of the IPO date (12/31/2023), Zomato's investment allocations are about 84% in India and 52.67% in Middle East, which adds up to more than half. The rest is spread across other regions. This indicates a strategic move to expand into international markets.
Looking at the previous conversation, the user asked about the three main ways Zomato earns revenue. In that chat, the assistant responded by saying that Zomato's main sources of revenue are delivery-based services in India and expanding into other regions like B2C and health care products. The financial data supports this because they're investing a significant portion of their proceeds into these areas to enhance their delivery capabilities and expand into new markets.
Now, the user provided a detailed list of Zomato's subsidiaries with their respective percentages invested in different regions. This adds more layers to Zomato's revenue streams. However, since we were told that the previous conversation already covered the main ways Zomato earns revenue, I should focus on those three points: primarily through delivery-based services (India), expanding into B2C and other essential products, and enhancing technological capabilities.
I should make sure these are accurate based on the provided financial data. Each subsidiary's investment in different regions seems to support this conclusion. For example, they have a 100% investment in India for Zomato Entertainment, which is their primary service area. Then there are subsidiaries like TongueStun and Carthero Technologies that focus on personal care products, which would be part of their delivery offerings but expanded into B2C markets.
They also mention Jogo Technologies and others with a 64.6% investment in Middle East, suggesting they're looking to expand further into international markets beyond India, perhaps through these other regions. The fact that they have significant investments in health care products (Zomato Foods) as well indicates another revenue source beyond just delivery.
Moreover, their subsidiaries like Zomato Middle East FZ-LLC and PT Zomato Media Indonesia are likely involved in marketing, media, or expanded distribution, which could also contribute to revenue from B2C segments. The strategic expansion into these areas aligns with the financial allocations and strategic focus on international markets.
In summary, while there might be additional revenue streams through other subsidiaries, the three main ways Zomato earns revenue are primarily through delivery-based services in India, expanding into B2C and other essential products, and enhancing their technological capabilities. The provided data supports these points by showing significant investments in multiple regions, including India where most operations are based.
```

#### GPT-4o Response:
```
Zomato earns revenue through three main business segments:
1. **Food Delivery**: This is the primary revenue source, accounting for about 71% of Zomato's revenue. Zomato earns commissions from restaurant partners, typically ranging from 15% to 25% of the order value. Additionally, while Zomato collects delivery charges from customers, these are not included in the revenue or costs in the P&L statement post-October 2019.
2. **Dining Out**: This segment contributes about 19% of Zomato's revenue. It includes revenue from advertisements from restaurant partners and a paid membership program called Zomato Pro and Pro+, which offers discounts at select restaurants.
3. **Hyperpure**: This is a B2B supplies business, although specific revenue details from this segment are not provided in the content.
Additionally, Zomato has operations in overseas markets, including a food delivery business in the UAE and an advertising-food discovery business in multiple countries, which collectively account for 9.4% of total revenues in FY21. However, the company is in the process of exiting
```



## Model Analysis

### Strengths and Weaknesses

#### DeepSeek R1

##### ✅ Strengths
- Excels in deep reasoning and step-by-step analysis, making it valuable for complex problem-solving
- More cost-effective, providing AI capabilities at a fraction of GPT-4o's price
- Stronger performance in math and coding tasks due to structured logical processing

##### ❌ Weaknesses
- Slower response time (850ms vs. GPT-4o's 232ms), making it less efficient for real-time interactions
- Occasional inaccuracies, as it prioritizes reasoning over concise fact retrieval
- Lacks multi-modal capabilities (text, image, audio, video) like GPT-4o

#### GPT-4o

##### ✅ Strengths
- Highly accurate responses with fact-based precision, making it ideal for straightforward knowledge retrieval
- Blazing fast latency (232ms) enables real-time applications like chatbots and voice assistants
- Supports multi-modal inputs and outputs (text, images, audio, and video), expanding its use cases

##### ❌ Weaknesses
- More expensive, costing up to 4.6x more than DeepSeek R1
- Slightly weaker in math and coding tasks, as it prioritizes response speed over structured reasoning
- Limited in step-by-step deep reasoning compared to DeepSeek R1

## Final Verdict: Which Model is Better for RAG?

### Model Selection Guide
- If you need cost-effective, in-depth analytical reasoning → **Choose DeepSeek R1**
- If you prioritize speed, accuracy, and multi-modal support → **Choose GPT-4o**
- For RAG tasks requiring step-by-step business intelligence analysis → **DeepSeek R1 is better**

## Conclusion
- Both DeepSeek R1 and GPT-4o are powerful AI models with unique strengths
- DeepSeek R1 is a game-changer for cost-effective AI inference, excelling in structured reasoning and math-heavy applications
- GPT-4o dominates in speed, factual accuracy, and general knowledge, making it ideal for real-time AI solutions

### Final Thought
The choice depends on your specific use case:
- For affordable deep reasoning → DeepSeek R1
- For speed and precision → GPT-4o

🔹 Try both models and share your experience!
