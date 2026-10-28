from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic:str)->dict:

    state = {}

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages":[("user",f"Find recent, reliable and detailed information about:{topic}")]
    })

    state['search_results'] = search_result['messages'][-1].content

    reader_agent=build_reader_agent()
    result=reader_agent.invoke({
        "messages":[("user",
                     f"Based on the following search results about '{topic}'"
                     f"pick the most relevant url and scrape it for deeper content.\n\n"
                     f"Search results:\n{state['search_results'][:800]}")]
    })

    state['scraped_content'] = result['messages'][-1].content

    print("scraped content",state['scraped_content'])

    research_combined = (
        f"SEARCH RESULTS: \n {state['search_results']}"
        f"DETAILED SCRAPED CONTENT: \n {state['scraped_content']}"
    )

    state['report'] = writer_chain.invoke({
        "topic":topic,
        "research":research_combined
    })

    state['feedback'] = critic_chain.invoke({
        "report":state['report']
    })

    return state

if __name__ == "__main__":
    topic = input("/n Enter research topic")
    run_research_pipeline(topic=topic)