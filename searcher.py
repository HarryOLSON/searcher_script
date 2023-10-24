from serpapi import GoogleSearch


class SerpApiSearcher:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def get_serpapi_data(self, keyword, city):
        params = {
            "engine": "google_maps",
            "q": f"{keyword} {city}",
            "hl": "en",
            "type": "search",
            "api_key": self.api_key
        }

        search = GoogleSearch(params)
        data = search.get_dict()
        return data

    def extract_serpapi_data(self, data):
        results = []
        for item in data.get('local_results', []):
            position = item.get("position")
            business_name = item.get("title")
            url = item.get("link")
            reviews = item.get("reviews")
            results.append(
                {
                    "Ranking Position": position,
                    "Business Name": business_name,
                    "URL": url,
                    "Number of Reviews": reviews
                }
            )
        return self.get_business_by_rank(results)

    @staticmethod
    def get_business_by_rank(data):
        return sorted(data, key=lambda item: item['Ranking Position'], reverse=True)
