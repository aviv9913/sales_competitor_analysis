# Project Documentation

## Approach and Choices Made

### Data Collection
Collecting data using `praw` and reddit api.
Decided which parts of the post is relevant for the task: title, text, score (upvotes), creation_time_utc, id, url, author_name, comments
Created a pydantic model.
Each post in a separate json file.
Searching posts using reddit search api and limited to 20 posts.

### Post Summarization
We implemented a summarization module using OpenAI's GPT-4o-mini model to generate summary of each post. 
I chose GPT-4o-mini since it's the most value/money model available in OpenAI API.
I needed to run the summarization task on all posts so I needed to conserve money and get a decent summary.
The summarizer extracts key information such as customer status, sentiment, advantages, and disadvantages and finds if the post contains a competitor.
The summarized data is in a json file for each post.
I used a json output format to keep the output structured and concise.

### Actionable Posts
The summarized posts were converted to pandas dataframe from the json files.
I filtered the post based on predetermine conditions.
Each filtered post was sent to GPT-4o for actionability analysis.
I chose Gpt-4o since I thought deciding on further action is a more difficult job for LLM than summarization and it runs on fewer data so I can `spent` more money on it.
I used a json output format to keep the output structured and concise.

### Report Generation
The report generation module aggregates the summarized data to produce a comprehensive market analysis report. 
This report includes sections on top competitors, best advantages, best disadvantages, and overall customer satisfaction. 
The data was aggregated using pandas to try to provide a few aspects from the posts.
The aggregated data was sent to Gpt-4o for report generation in a markdown file.
Markdown allows the report to have more visual information (in the cost of more output tokens) make the data more readable.
I added a actionable insights at the end.

### Code Structure
- `data_collection_main.py`: Script for collecting data from Reddit.
- `post_summarization.py`: Module for summarizing Reddit posts.
- `generate_report.py`: Script for generating the market analysis report.
- `find_actionable_post.py`: Script to filter posts for actionable ones and generate post action.
- `sales_competitor_analysis`: Module to keep the code organized, contains `data_models` and classes used in the scripts.
- `data\`: Contains the raw and processed posts by folder and file.
- `notebooks\`: Contains playground notebooks used for investigating the API, prompts and other functionality.

## Next Steps for Improvement

### Enhanced Data Collection
- **Broader Data Sources**: Integrate additional data sources such as Twitter, LinkedIn, and industry forums to provide a more comprehensive analysis.
- **Real-time Data Collection**: Implement real-time data collection to keep the analysis up-to-date with the latest discussions.

### Improved Summarization
- **More Context**: Use both comments and poster (the person who posted the post) information in the summarization.

### Performance Optimization
- **Scalability**: Optimize the codebase for scalability to handle larger datasets and more complex analyses.
- **Efficiency**: Improve the efficiency of data processing and summarization to reduce the overall runtime of the solution.

### Technical Dept
- **Configuration Manager**: Setup a configuration manager to handle secrets, and other configs.
- **Robustness**: Better handle errors in the code in a way that the program can continue to run without interference.
- **Consistency**: Better structure prompts and classes.
- **Observability**: Emit better logs from all parts of the codebase.