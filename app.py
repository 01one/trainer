from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import secrets
import json
import os
import uuid

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
DATA_FILE = 'data/tutorials.json'

def get_internet_tutorial():
    return [{
        "id": str(uuid.uuid4()),
        "title": "The Journey of the Internet",
        "steps": [
			{
				"instruction": "<h3 class='text-xl font-bold mb-2'>1. 1969: The ARPANET</h3><p class='mb-4'>The internet began as a US government-funded research network developed by ARPA. It connected universities to explore reliable communication. The first message sent was 'LO' (intended to be 'LOGIN', but the system crashed).</p><p class='font-bold text-blue-700'>Click the 'Interface Message Processor' (IMP) to send the first packet.</p>",
				"mockup": "<div class='bg-zinc-800 p-10 rounded-xl shadow-2xl text-center w-full max-w-2xl border-4 border-zinc-600'> <h2 class='text-green-500 font-mono text-xl mb-6 tracking-tighter'>[ UCLA NODE - OCT 1969 ]</h2> <div class='interactive-hotspot bg-zinc-700 p-8 rounded-lg border-2 border-green-500/50 shadow-[0_0_15px_rgba(34,197,94,0.2)] cursor-pointer hover:bg-zinc-600 transition-all' data-target-step='2'> <div class='text-6xl mb-4'>📠</div> <p class='text-green-400 font-mono font-bold'>SEND PACKET: 'LOGIN'</p> </div> <div class='mt-8 text-zinc-500 font-mono text-xs'>System Status: ONLINE</div></div>"
			},
            {
                "instruction": "<h3 class='text-xl font-bold mb-2'>2. 1983: TCP/IP</h3><p class='mb-4'>To let different networks talk to each other, a universal 'language' was needed. This became TCP/IP.</p><p class='font-bold text-blue-700'>Click the 'Protocol' icon to standardize the network.</p>",
                "mockup": "<div class='bg-blue-900 p-10 rounded-3xl shadow-xl text-center w-full max-w-2xl text-white'> <h2 class='text-2xl font-bold mb-8'>Global Standardization</h2> <div class='flex justify-center gap-6'> <div class='bg-blue-800 p-6 rounded-xl border border-blue-400 opacity-50'>Network A</div> <div class='interactive-hotspot bg-white text-blue-900 p-8 rounded-full font-black shadow-2xl cursor-pointer hover:scale-110 transition-transform' data-target-step='3'>TCP/IP</div> <div class='bg-blue-800 p-6 rounded-xl border border-blue-400 opacity-50'>Network B</div> </div> <p class='mt-8 text-blue-200 italic font-medium'>Connecting the world's networks...</p></div>"
            },
            {
                "instruction": "<h3 class='text-xl font-bold mb-2'>3. 1991: The World Wide Web</h3><p class='mb-4'>Tim Berners-Lee at CERN invented the Web. It wasn't 'the internet' itself, but a way to browse info using hyperlinks.</p><p class='font-bold text-blue-700'>Click the 'Blue Hyperlink' to navigate to the first web page.</p>",
                "mockup": "<div class='bg-white p-10 rounded-none border border-gray-300 shadow-md text-left w-full max-w-2xl font-serif'> <h2 class='text-3xl font-bold border-b-2 border-black mb-4'>World Wide Web</h2> <p class='mb-4'>The WorldWideWeb (W3) is a wide-area hypermedia information retrieval initiative...</p> <div class='interactive-hotspot text-blue-700 underline decoration-blue-700 font-bold cursor-pointer text-xl' data-target-step='4'>Click here to see the Project Summary</div> </div>"
            },
            {
                "instruction": "<h3 class='text-xl font-bold mb-2'>4. 1993: Mosaic & Browsers</h3><p class='mb-4'>Mosaic was the first browser to display images inline with text. Suddenly, the web became visual and fun.</p><p class='font-bold text-blue-700'>Click the 'Globe' to load the graphical interface.</p>",
                "mockup": "<div class='bg-gray-200 p-2 rounded-t-xl border border-gray-400 flex gap-2'> <div class='w-3 h-3 bg-red-400 rounded-full'></div><div class='w-3 h-3 bg-yellow-400 rounded-full'></div><div class='w-3 h-3 bg-green-400 rounded-full'></div> </div> <div class='bg-white p-10 border border-gray-400 shadow-xl text-center w-full max-w-2xl'> <div class='interactive-hotspot cursor-pointer group' data-target-step='5'> <div class='text-8xl mb-4 group-hover:rotate-12 transition-transform'>🌍</div> <h2 class='text-2xl font-black italic text-blue-900 tracking-tighter'>NCSA MOSAIC</h2> </div> <p class='mt-6 text-gray-500 font-bold uppercase text-xs tracking-widest'>The web is now visual</p> </div>"
            },
            {
                "instruction": "<h3 class='text-xl font-bold mb-2'>5. 1998: The Google Era</h3><p class='mb-4'>As the web grew, finding things became impossible. Google's PageRank algorithm organized the world's information.</p><p class='font-bold text-blue-700'>Type your query and click 'Google Search'.</p>",
                "mockup": "<div class='bg-white p-12 rounded-3xl shadow-sm border border-gray-100 text-center w-full max-w-2xl'> <h1 class='text-5xl font-bold mb-8'><span class='text-blue-500'>G</span><span class='text-red-500'>o</span><span class='text-yellow-500'>o</span><span class='text-blue-500'>g</span><span class='text-green-500'>l</span><span class='text-red-500'>e</span></h1> <div class='w-full max-w-md mx-auto h-12 border rounded-full shadow-sm flex items-center px-4 mb-6'> <div class='text-gray-400 mr-2'><i class='fas fa-search'></i></div> <div class='text-gray-300'>How does the internet work?</div> </div> <button class='interactive-hotspot bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium px-6 py-2 rounded shadow-sm transition-all' data-target-step='6'>Google Search</button> </div>"
            },
            {
                "instruction": "<h3 class='text-xl font-bold mb-2'>6. 2004: Web 2.0 (Social)</h3><p class='mb-4'>The web moved from 'Read-Only' to 'Read-Write'. People began creating content on Facebook, YouTube, and Twitter.</p><p class='font-bold text-blue-700'>Click the 'Like' button to interact with the post.</p>",
                "mockup": "<div class='bg-white p-8 rounded-xl shadow-md border border-gray-200 text-left w-full max-w-md'> <div class='flex items-center gap-3 mb-4'> <div class='w-10 h-10 bg-blue-500 rounded-full'></div> <div><div class='font-bold'>User_2004</div><div class='text-xs text-gray-500'>2 minutes ago</div></div> </div> <p class='mb-6'>Just joined the social revolution! The web is about people now. 🚀</p> <div class='flex border-t pt-4'> <div class='interactive-hotspot text-blue-600 font-bold cursor-pointer hover:bg-blue-50 px-4 py-2 rounded transition-colors' data-target-step='7'><i class='fas fa-thumbs-up mr-2'></i>Like</div> </div> </div>"
            },
            {
                "instruction": "<h3 class='text-xl font-bold mb-2'>7. 2007: The Mobile Web</h3><p class='mb-4'>The iPhone changed everything. The internet was no longer a place you 'went' to on a desk; it was in your pocket 24/7.</p><p class='font-bold text-blue-700'>Click the 'App Icon' to launch the mobile web.</p>",
                "mockup": "<div class='w-64 h-[450px] bg-black rounded-[3rem] border-[6px] border-gray-800 shadow-2xl relative p-4 flex flex-col items-center justify-center'> <div class='absolute top-0 left-1/2 -translate-x-1/2 w-24 h-6 bg-gray-800 rounded-b-xl'></div> <div class='interactive-hotspot w-20 h-20 bg-gradient-to-br from-purple-500 to-blue-600 rounded-2xl shadow-xl flex items-center justify-center text-white text-3xl cursor-pointer hover:scale-110 transition-transform' data-target-step='8'> <i class='fas fa-cloud'></i> </div> <div class='mt-4 text-white font-bold text-xs'>Mobile Net</div> <div class='absolute bottom-2 left-1/2 -translate-x-1/2 w-10 h-1 bg-gray-600 rounded-full'></div> </div>"
            },
            {
                "instruction": "<h3 class='text-xl font-bold mb-2'>8. 2010s: The Cloud</h3><p class='mb-4'>Software moved off your computer and into 'The Cloud'. Netflix, Spotify, and AWS became the backbone of our lives.</p><p class='font-bold text-blue-700'>Click the 'Play' button to stream from the cloud.</p>",
                "mockup": "<div class='bg-zinc-900 p-10 rounded-2xl shadow-2xl text-center w-full max-w-2xl border border-zinc-700'> <h2 class='text-red-600 font-black text-4xl mb-10 tracking-tighter'>CLOUD STREAM</h2> <div class='interactive-hotspot bg-white/10 p-12 rounded-full inline-block cursor-pointer hover:bg-white/20 transition-all' data-target-step='9'> <div class='text-6xl text-white ml-2'><i class='fas fa-play'></i></div> </div> <div class='mt-10 flex justify-center gap-4'> <div class='w-32 h-2 bg-red-600 rounded-full animate-pulse'></div> </div> </div>"
            },
            {
                "instruction": "<h3 class='text-xl font-bold mb-2'>9. 2023+: The AI Web</h3><p class='mb-4'>Internet search is becoming a conversation. Large Language Models (LLMs) like ChatGPT are redefining how we get info.</p><p class='font-bold text-blue-700'>Click the 'AI Sparkle' to generate the next chapter.</p>",
                "mockup": "<div class='bg-[#0a0a0a] p-10 rounded-3xl shadow-2xl text-center w-full max-w-2xl border border-purple-500/30'> <div class='text-purple-400 font-mono mb-4 text-sm tracking-widest'>NEURAL INTERFACE ACTIVE</div> <div class='interactive-hotspot cursor-pointer group' data-target-step='10'> <div class='text-7xl mb-6 group-hover:drop-shadow-[0_0_20px_rgba(168,85,247,0.6)] transition-all'>✨</div> <div class='bg-zinc-800 p-4 rounded-xl text-zinc-400 font-mono text-sm border border-zinc-700 italic'>\"Explain the future of the internet...\"</div> </div> </div>"
            },
            {
                "instruction": "<h3 class='text-xl font-bold mb-2'>10. The Infinite Future</h3><p class='mb-4'>From a 50kbps military link to a global AI brain. The journey of the internet is the journey of human connection.</p><p class='font-bold text-blue-700'>Click 'Finish' to complete the module.</p>",
                "mockup": "<div class='text-center p-12 bg-white rounded-3xl shadow-xl border border-blue-100'> <div class='text-6xl mb-6 text-blue-600'><i class='fas fa-network-wired'></i></div> <h2 class='text-3xl font-bold mb-4'>Journey Complete</h2> <p class='text-gray-500 mb-8 max-w-md mx-auto italic'>The internet is no longer a tool we use; it is the environment we live in.</p> <button class='interactive-hotspot bg-blue-600 hover:bg-blue-700 text-white px-12 py-4 rounded-full font-bold shadow-lg transition-transform hover:-translate-y-1' data-target-step='99'>End Tutorial</button> </div>"
            }
        ]
    }]

def load_tutorials():
    if not os.path.exists(DATA_FILE):
        os.makedirs('data', exist_ok=True)
        default_data = get_internet_tutorial()
        save_tutorials(default_data)
        return default_data
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_tutorials(data):
    os.makedirs('data', exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index(): return render_template('index.html', tutorials=load_tutorials())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == 'admin' and request.form.get('password') == 'password':
            session['admin'] = True
            return redirect(url_for('admin'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if not session.get('admin'): return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/tutorial/<tut_id>')
def tutorial(tut_id): return render_template('tutorial.html', tut_id=tut_id)

@app.route('/api/tutorials', methods=['GET', 'POST'])
def api_tutorials():
    if request.method == 'GET': return jsonify(load_tutorials())
    if not session.get('admin'): return jsonify({'error': 'Unauthorized'}), 401
    
    tutorials, new_data = load_tutorials(), request.json
    if new_data.get('id'):
        for i, tut in enumerate(tutorials):
            if tut['id'] == new_data['id']:
                tutorials[i] = new_data
                break
    else:
        new_data['id'] = str(uuid.uuid4())
        tutorials.append(new_data)
        
    save_tutorials(tutorials)
    return jsonify({'success': True})

@app.route('/api/tutorials/<tut_id>', methods=['DELETE'])
def api_delete_tutorial(tut_id):
    if not session.get('admin'): return jsonify({'error': 'Unauthorized'}), 401
    save_tutorials([t for t in load_tutorials() if t['id'] != tut_id])
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
