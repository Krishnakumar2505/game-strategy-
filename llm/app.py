from flask import Flask, render_template, request, jsonify
from langchain_groq import ChatGroq

app = Flask(__name__)

API_KEY = "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"
llm = ChatGroq(api_key=API_KEY)

chess_strategy_data = [
    {"id": 1, "opening": "Sicilian Defense", "type": "Aggressive", "key_moves": "1.e4 c5", "goal": "Control center, counterattack"},
    {"id": 2, "opening": "French Defense", "type": "Defensive", "key_moves": "1.e4 e6", "goal": "Solid structure, counter center"},
    {"id": 3, "opening": "Ruy Lopez", "type": "Positional", "key_moves": "1.e4 e5 2.Nf3 Nc6 3.Bb5", "goal": "Apply pressure on the center"},
    {"id": 4, "opening": "King's Indian Defense", "type": "Flexible", "key_moves": "1.d4 Nf6 2.c4 g6", "goal": "Control dark squares, counterattack"},
    {"id": 5, "opening": "Queen's Gambit", "type": "Strategic", "key_moves": "1.d4 d5 2.c4", "goal": "Trade central pawn, develop pieces"},
    {"id": 6, "opening": "Caro-Kann Defense", "type": "Solid", "key_moves": "1.e4 c6", "goal": "Control center, develop safely"},
    {"id": 7, "opening": "Grünfeld Defense", "type": "Dynamic", "key_moves": "1.d4 Nf6 2.c4 g6 3.Nc3 d5", "goal": "Counterattack center with pawns"},
    {"id": 8, "opening": "English Opening", "type": "Flank", "key_moves": "1.c4", "goal": "Flexible pawn structure, flank attack"},
    {"id": 9, "opening": "Nimzo-Indian Defense", "type": "Strategic", "key_moves": "1.d4 Nf6 2.c4 e6 3.Nc3 Bb4", "goal": "Control center, pressure pawn"},
    {"id": 10, "opening": "Scandinavian Defense", "type": "Aggressive", "key_moves": "1.e4 d5", "goal": "Immediate counterattack on center"},
    {"id": 11, "opening": "Pirc Defense", "type": "Flexible", "key_moves": "1.e4 d6 2.d4 Nf6", "goal": "Develop pieces, maintain flexibility"},
    {"id": 12, "opening": "Vienna Game", "type": "Aggressive", "key_moves": "1.e4 e5 2.Nc3", "goal": "Rapid development, attack center"},
    {"id": 13, "opening": "Alekhine Defense", "type": "Counterattacking", "key_moves": "1.e4 Nf6", "goal": "Provoke weaknesses, counterattack"},
    {"id": 14, "opening": "London System", "type": "Systematic", "key_moves": "1.d4 d5 2.Nf3 Nf6 3.Bf4", "goal": "Control center with setup"},
    {"id": 15, "opening": "Catalan Opening", "type": "Positional", "key_moves": "1.d4 Nf6 2.c4 e6 3.g3", "goal": "Control center, fianchetto bishop"},
    {"id": 16, "opening": "Italian Game", "type": "Classical", "key_moves": "1.e4 e5 2.Nf3 Nc6 3.Bc4", "goal": "Attack f7, rapid development"},
    {"id": 17, "opening": "Scotch Game", "type": "Open", "key_moves": "1.e4 e5 2.Nf3 Nc6 3.d4", "goal": "Open center, rapid play"},
    {"id": 18, "opening": "Benoni Defense", "type": "Aggressive", "key_moves": "1.d4 Nf6 2.c4 c5", "goal": "Counter center, unbalanced position"},
    {"id": 19, "opening": "Benko Gambit", "type": "Gambit", "key_moves": "1.d4 Nf6 2.c4 c5 3.d5 b5", "goal": "Sacrifice pawn for open files"},
    {"id": 20, "opening": "Dutch Defense", "type": "Aggressive", "key_moves": "1.d4 f5", "goal": "Control center, kingside attack"},
    {"id": 21, "opening": "Four Knights Game", "type": "Classical", "key_moves": "1.e4 e5 2.Nf3 Nc6 3.Nc3 Nf6", "goal": "Solid development, control center"},
    {"id": 22, "opening": "King's Gambit", "type": "Gambit", "key_moves": "1.e4 e5 2.f4", "goal": "Sacrifice pawn, rapid kingside attack"},
    {"id": 23, "opening": "Czech Defense", "type": "Defensive", "key_moves": "1.e4 d6 2.d4 Nf6 3.Nd2", "goal": "Solid structure, defense"},
    {"id": 24, "opening": "Modern Defense", "type": "Flexible", "key_moves": "1.e4 g6", "goal": "Fianchetto bishop, flexible defense"},
    {"id": 25, "opening": "Tarrasch Defense", "type": "Strategic", "key_moves": "1.d4 d5 2.c4 e6 3.Nc3 c5", "goal": "Dynamic counterplay, pawn tension"},
    {"id": 26, "opening": "Petrov Defense", "type": "Defensive", "key_moves": "1.e4 e5 2.Nf3 Nf6", "goal": "Solid defense, exchange symmetry"},
    {"id": 27, "opening": "Philidor Defense", "type": "Defensive", "key_moves": "1.e4 e5 2.Nf3 d6", "goal": "Solid structure, slow buildup"},
    {"id": 28, "opening": "Giuoco Piano", "type": "Positional", "key_moves": "1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5", "goal": "Slow buildup, positional play"},
    {"id": 29, "opening": "Evans Gambit", "type": "Gambit", "key_moves": "1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.b4", "goal": "Sacrifice pawn for rapid attack"},
    {"id": 30, "opening": "Reti Opening", "type": "Hypermodern", "key_moves": "1.Nf3", "goal": "Control center from distance"},
    {"id": 31, "opening": "Fried Liver Attack", "type": "Aggressive", "key_moves": "1.e4 e5 2.Nf3 Nc6 3.Bc4 Nf6 4.Ng5", "goal": "Attack weak f7 square"},
    {"id": 32, "opening": "Blackmar-Diemer Gambit", "type": "Gambit", "key_moves": "1.d4 d5 2.e4", "goal": "Sacrifice pawn, rapid development"},
    {"id": 33, "opening": "Bird's Opening", "type": "Flank", "key_moves": "1.f4", "goal": "Kingside control, flexible attack"},
    {"id": 34, "opening": "Stonewall Attack", "type": "Strategic", "key_moves": "1.d4 e6 2.e3 f4", "goal": "Solid pawn structure, kingside attack"},
    {"id": 35, "opening": "Colle System", "type": "Systematic", "key_moves": "1.d4 d5 2.Nf3 Nf6 3.e3", "goal": "Setup structure, solid play"},
    {"id": 36, "opening": "Trompowsky Attack", "type": "Aggressive", "key_moves": "1.d4 Nf6 2.Bg5", "goal": "Pin knight, create imbalance"},
    {"id": 37, "opening": "English Defense", "type": "Flank", "key_moves": "1.d4 e6 2.c4 b6", "goal": "Fianchetto bishop, flank play"},
    {"id": 38, "opening": "Polish Opening", "type": "Flank", "key_moves": "1.b4", "goal": "Flank attack, early pawn push"},
    {"id": 39, "opening": "Zukertort Opening", "type": "Flexible", "key_moves": "1.Nf3 d5 2.b3", "goal": "Flexible development, flank play"},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_chess_strategy', methods=['POST'])
def get_chess_strategy():
    data = request.get_json()
    opening_name = data.get('opening_name', '').lower()
    
    if not opening_name:
        return jsonify({'error': 'Opening name is required'}), 400
    
    for strategy in chess_strategy_data:
        if strategy['opening'].lower() == opening_name:
            return jsonify(strategy)
    
    return jsonify({'error': 'Opening not found'})

if __name__ == '__main__':
    app.run(debug=True)
