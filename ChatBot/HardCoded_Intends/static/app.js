//Main JS App

class Chatbox {
    constructor(){
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.message = [];
    }


    display(){
        const {openButton, chatBox, sendButton} = this.args;

        // Check if any of the elements are missing
        if (!openButton || !chatBox || !sendButton) {
            console.error("One or more required elements are missing.");
            //return; // Exit the function if any element is missing chatBox is missing!!!
        }

        openButton.addEventListener('click', ()=>this.toggleState(chatBox))
        sendButton.addEventListener('click', ()=>this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener('keyup', ({key})=>{
            if (key == "Enter"){
                this.onSendButton(chatBox)
            }
        })

    }

    toggleState(chatbox){
        this.state = !this.state;
    
        // Add a debug log
        console.log("toggleState triggered, new state:", this.state);
        
        if(this.state){
            chatbox.classList.add('chatbox--active')
        }  else {
            chatbox.classList.remove('chatbox--active')
        }
    }


    onSendButton(chatbox){
        var text_field = chatbox.querySelector('input');
        let txt1 = text_field.value
        if(txt1 === ""){
            return;
        }

        //object msg1
        let msg1 = {name: "User", message: txt1}
        this.message.push(msg1);

        //'localhost:5000/predict' you can hard-code it as well 
        //example: 
        // fetch('http://xxx.x.x.x:5000/predict', {method...,} ).then...

        
        fetch($SCRIPT_ROOT + '/predict', {  //SCRIPT_ROOT is var defined in the html script section
            method: 'POST',
            body: JSON.stringify({message: txt1}),
            mode: 'cors',  //cross origin resource sharing
            headers: {
                'Content-Type': 'application/json'
            },

        }) //return promise
        .then(resp => resp.json())
        .then(resp => {
            let msg2 = {name: "Bot", message: resp.answer}
            //push to messages array
            this.message.push(msg2);
            this.updateChatText(chatbox)
            text_field.value =''
        }).catch((error) => {
            console.log('Error: ', error)
            this.updateChatText(chatbox)
            text_field.value = ''
          });

    }




    updateChatText(chatbox){
    var html = '';
    this.message.slice().reverse().forEach(function(item, ){ //index:number
        if (item.name == "Bot"){
            html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
        }
        else{
            html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
        }
    });

    const chatmessage = chatbox.querySelector('.chatbox__messages');
    chatmessage.innerHTML = html;

    }



}


document.getElementById('toggleMode').addEventListener('click', function() {
    var body = document.body;
    
    if (body.style.background == 'white') {
        body.style.background = '#1e1d1d';
    } else {
        body.style.background = 'white';
    }
});


//initialize new obj from the class

document.addEventListener("DOMContentLoaded", function(event) { 
    const chatbox = new Chatbox();
    chatbox.display();
  });

