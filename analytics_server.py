from flask import Flask, send_from_directory, request, jsonify
import requests
import praw
import json
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import ssl
import socket
import whois
from datetime import datetime
import threading
import time
from textblob import TextBlob

app = Flask(__name__, static_folder='.')

# Reddit API credentials
REDDIT_CLIENT_ID = xxxxxxxxxxxxxx"
REDDIT_CLIENT_SECRET = "XXXXXXXXXXXXXXXXXXXXXXX"
REDDIT_USER_AGENT = "XXXXXXXXXXXXXXX"
REDDIT_USERNAME = "XXXXXXXXXXX"
REDDIT_PASSWORD = "XXXXXXXXXXXXXXXXXX"

# Initialize Reddit client
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD
)

@app.route('/')
def serve_game():
    return send_from_directory('.', 'game.html')

@app.route('/analytics')
def serve_analytics():
    return send_from_directory('.', 'analytics.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/analyze-website', methods=['POST'])
def analyze_website():
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        analysis_results = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'basic_info': get_basic_website_info(url),
            'seo_analysis': get_seo_analysis(url),
            'technical_audit': get_technical_audit(url),
            'domain_info': get_domain_info(url),
            'security_check': get_security_check(url)
        }
        
        return jsonify(analysis_results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-reddit', methods=['POST'])
def analyze_reddit():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        limit = min(data.get('limit', 50), 100)  # Cap at 100
        
        reddit_results = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'search_results': search_reddit_posts(query, limit),
            'sentiment_analysis': get_reddit_sentiment(query, limit // 2),
            'subreddit_analysis': get_subreddit_mentions(query)
        }
        
        return jsonify(reddit_results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai-chat', methods=['POST'])
def ai_chat():
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Call local AI model
        ai_response = call_local_ai(message)
        
        return jsonify({
            'response': ai_response,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_basic_website_info(url):
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        soup = BeautifulSoup(response.text, 'html.parser')
        
        return {
            'status_code': response.status_code,
            'title': soup.title.string if soup.title else 'No title found',
            'meta_description': soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else 'No meta description',
            'h1_tags': [h1.get_text().strip() for h1 in soup.find_all('h1')],
            'h2_tags': [h2.get_text().strip() for h2 in soup.find_all('h2')][:5],  # First 5 H2s
            'images_without_alt': len([img for img in soup.find_all('img') if not img.get('alt')]),
            'total_images': len(soup.find_all('img')),
            'internal_links': len([a for a in soup.find_all('a', href=True) if urlparse(a['href']).netloc == '' or urlparse(url).netloc in a['href']]),
            'external_links': len([a for a in soup.find_all('a', href=True) if urlparse(a['href']).netloc != '' and urlparse(url).netloc not in a['href']])
        }
    except Exception as e:
        return {'error': str(e)}

def get_seo_analysis(url):
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for common SEO elements
        canonical = soup.find('link', rel='canonical')
        robots_meta = soup.find('meta', attrs={'name': 'robots'})
        schema_scripts = soup.find_all('script', type='application/ld+json')
        
        return {
            'has_canonical': bool(canonical),
            'canonical_url': canonical['href'] if canonical else None,
            'robots_meta': robots_meta['content'] if robots_meta else None,
            'structured_data_scripts': len(schema_scripts),
            'title_length': len(soup.title.string) if soup.title else 0,
            'meta_description_length': len(soup.find('meta', attrs={'name': 'description'})['content']) if soup.find('meta', attrs={'name': 'description'}) else 0,
            'h1_count': len(soup.find_all('h1')),
            'has_sitemap': check_sitemap(url),
            'has_robots_txt': check_robots_txt(url)
        }
    except Exception as e:
        return {'error': str(e)}

def get_technical_audit(url):
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        return {
            'response_time': response.elapsed.total_seconds(),
            'content_type': response.headers.get('content-type', ''),
            'server': response.headers.get('server', ''),
            'content_length': len(response.content),
            'compression': 'gzip' in response.headers.get('content-encoding', ''),
            'cache_control': response.headers.get('cache-control', ''),
            'last_modified': response.headers.get('last-modified', ''),
            'etag': response.headers.get('etag', '')
        }
    except Exception as e:
        return {'error': str(e)}

def get_domain_info(url):
    try:
        domain = urlparse(url).netloc
        domain_info = whois.whois(domain)
        
        return {
            'domain': domain,
            'registrar': str(domain_info.registrar) if domain_info.registrar else 'Unknown',
            'creation_date': str(domain_info.creation_date) if domain_info.creation_date else 'Unknown',
            'expiration_date': str(domain_info.expiration_date) if domain_info.expiration_date else 'Unknown',
            'name_servers': domain_info.name_servers if domain_info.name_servers else []
        }
    except Exception as e:
        return {'error': str(e)}

def get_security_check(url):
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        headers = response.headers
        security_headers = {
            'strict_transport_security': headers.get('strict-transport-security'),
            'content_security_policy': headers.get('content-security-policy'),
            'x_frame_options': headers.get('x-frame-options'),
            'x_content_type_options': headers.get('x-content-type-options'),
            'referrer_policy': headers.get('referrer-policy')
        }
        
        # SSL Certificate check
        ssl_info = {}
        if url.startswith('https://'):
            try:
                hostname = urlparse(url).hostname
                context = ssl.create_default_context()
                with socket.create_connection((hostname, 443), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        cert = ssock.getpeercert()
                        ssl_info = {
                            'issuer': dict(x[0] for x in cert['issuer']),
                            'subject': dict(x[0] for x in cert['subject']),
                            'expires': cert['notAfter'],
                            'version': cert['version']
                        }
            except Exception as e:
                ssl_info = {'error': str(e)}
        
        return {
            'is_https': url.startswith('https://'),
            'security_headers': security_headers,
            'ssl_info': ssl_info
        }
    except Exception as e:
        return {'error': str(e)}

def check_sitemap(url):
    try:
        domain = urlparse(url).scheme + "://" + urlparse(url).netloc
        sitemap_url = domain + "/sitemap.xml"
        response = requests.get(sitemap_url, timeout=5)
        return response.status_code == 200
    except:
        return False

def check_robots_txt(url):
    try:
        domain = urlparse(url).scheme + "://" + urlparse(url).netloc
        robots_url = domain + "/robots.txt"
        response = requests.get(robots_url, timeout=5)
        return response.status_code == 200
    except:
        return False

def search_reddit_posts(query, limit):
    try:
        posts = []
        for submission in reddit.subreddit("all").search(query, limit=limit, sort='relevance'):
            posts.append({
                'title': submission.title,
                'subreddit': str(submission.subreddit),
                'score': submission.score,
                'upvote_ratio': submission.upvote_ratio,
                'num_comments': submission.num_comments,
                'created_utc': datetime.fromtimestamp(submission.created_utc).isoformat(),
                'url': submission.url,
                'permalink': f"https://reddit.com{submission.permalink}",
                'selftext': submission.selftext[:500] if submission.selftext else ''
            })
        return posts
    except Exception as e:
        return [{'error': str(e)}]

def get_reddit_sentiment(query, limit):
    try:
        posts = []
        sentiments = []
        
        for submission in reddit.subreddit("all").search(query, limit=limit, sort='top'):
            text = f"{submission.title} {submission.selftext}"
            blob = TextBlob(text)
            sentiment = blob.sentiment
            
            sentiments.append({
                'title': submission.title,
                'polarity': sentiment.polarity,
                'subjectivity': sentiment.subjectivity,
                'score': submission.score
            })
        
        if sentiments:
            avg_polarity = sum(s['polarity'] for s in sentiments) / len(sentiments)
            avg_subjectivity = sum(s['subjectivity'] for s in sentiments) / len(sentiments)
            
            return {
                'average_sentiment': {
                    'polarity': avg_polarity,
                    'subjectivity': avg_subjectivity,
                    'sentiment_label': 'Positive' if avg_polarity > 0.1 else 'Negative' if avg_polarity < -0.1 else 'Neutral'
                },
                'individual_sentiments': sentiments[:10]  # Top 10
            }
        else:
            return {'error': 'No posts found for sentiment analysis'}
    
    except Exception as e:
        return {'error': str(e)}

def get_subreddit_mentions(query):
    try:
        subreddit_counts = {}
        for submission in reddit.subreddit("all").search(query, limit=50):
            subreddit_name = str(submission.subreddit)
            subreddit_counts[subreddit_name] = subreddit_counts.get(subreddit_name, 0) + 1
        
        # Sort by count
        sorted_subreddits = sorted(subreddit_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'total_subreddits': len(sorted_subreddits),
            'top_subreddits': sorted_subreddits[:10],
            'total_mentions': sum(subreddit_counts.values())
        }
    except Exception as e:
        return {'error': str(e)}

def call_local_ai(message):
    try:
        payload = {
            "model": "google/gemma-3-12b",
            "messages": [
                {"role": "system", "content": "You are an amazing analyst that specializes in SEO and online visibility."},
                {"role": "user", "content": message}
            ],
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": False  # Set to False for simpler handling
        }
        
        response = requests.post(
            "http://127.0.0.1:1234/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"Error: AI service returned status {response.status_code}"
    
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to local AI service. Make sure it's running on http://127.0.0.1:1234"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    print("Starting Analytics Server...")
    print("Game available at: http://localhost:7777/")
    print("Analytics Dashboard at: http://localhost:7777/analytics")
    app.run(host='0.0.0.0', port=7777, debug=True)