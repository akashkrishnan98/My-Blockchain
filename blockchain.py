import json
import datetime
import hashlib
from flask import Flask,jsonify

class Blockchain:
    
    def __init__(self):
        self.chain=[]
        self.create_block(proof=0,previous_hash=0)
    
    def create_block(self,proof,previous_hash):
        block={'index':len(self.chain)+1,
               'timestamp':str(datetime.datetime.now()),
               'proof': proof,
               'previous_hash':previous_hash,
               }
        self.chain.append(block)
        return block
        
    def get_previous_block(self):
        return self.chain[-1]
    
    def hash(self,previous_proof):
        new_proof=1
        while True:
            hash_operation=hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]=='0000':
                return new_proof
            else:
                new_proof+=1
    
    def get_hash(self,block):
        encoded_block=json.dumps(block).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def chain_valid(self):
        block_index=1
        prev_block=self.chain[0]
        while block_index<len(self.chain):
            block=self.chain[block_index]
            previous_proof=prev_block['proof']
            if block['previous_hash']!=self.get_hash(prev_block):
                return False
            hash_operation=hashlib.sha256(str(block['proof']**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]!='0000':
                return False
            prev_block=block
            block_index+=1
        return True
        
blockchain=Blockchain()

app=Flask(__name__)

@app.route('/mine_block',methods=['GET'])
def mine_block():
    prev_block=blockchain.get_previous_block()
    prev_proof=prev_block['proof']
    proof=blockchain.hash(prev_proof)
    previous_hash=blockchain.get_hash(prev_block)
    block=blockchain.create_block(proof,previous_hash)
    
    #intentional index chain to invalidate chain
    if block['index']==5:
        blockchain.chain[0]['index']=2
    response={'msg':'Congrats, mined successfully',
              'index':block['index'],
              'timestamp':block['timestamp'],
              'proof':block['proof'],
              'previous_hash':block['previous_hash'],
              'this_hash':blockchain.get_hash(block)}
    return jsonify(response), 200

@app.route('/display_chain',methods=['GET'])
def display_chain():
    response={'chain length':len(blockchain.chain),
             'chain': blockchain.chain}
    return jsonify(response), 200

@app.route('/is_chain_valid',methods=['GET'])
def is_chain_valid():
    response={'msg':blockchain.chain_valid()}
    return jsonify(response),200

app.run(host='0.0.0.0',port=5000)

