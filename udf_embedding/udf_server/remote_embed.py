import requests



class RemoteEmbedingClient():

    def __init__(self) -> None:
        self.url = 'https://api.jina.ai/v1/embeddings'

        self.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer jina_41797e81e9b64f7c85efd97c71d6c14fgCd83mxQzyx_1REXcSN-hzge4Q6l'
        }
        
        self.model = 'jina-embeddings-v2-small-en'
        
    def get_params(self, input):
        data = {
        'input': [input],
        'model': self.model
        }
        return data
    
    def do_embed(self, str):
        response = requests.post(self.url, headers=self.headers, json=self.get_params(str))
        json_data = response.json()
        embedding = json_data['data'][0]['embedding']
        return embedding
    



if __name__ == '__main__':
    client = RemoteEmbedingClient()
    res = client.do_embed('hello world')
    print(res)

'''
{
  "model": "jina-embeddings-v2-base-en", 
  "object": "list", 
  "usage": {
    "total_tokens": 14, 
    "prompt_tokens": 14
  }, 
  "data": [
    {
      "object": "embedding", 
      "index": 0, 
      "embedding": []
    }, 
    {
      "object": "embedding", 
      "index": 1, 
      "embedding": []
    }
  ]
}
'''