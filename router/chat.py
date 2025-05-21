from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from db.model import DbAdvertisement
from db.database import get_db

#begin Tina
router = APIRouter()
active_connections = {}

chat_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple Chat</title>
</head>
<body>
    <h1>Chat with another user</h1>
    <form onsubmit="sendMessage(event)">
        <label>Receiver User ID: <input type="text" id="receiverId" autocomplete="off" /></label><br>
        <label>Advertisement ID: <input type="text" id="adId" autocomplete="off" /></label><br>
        <input type="text" id="messageText" placeholder="Type your message..." autocomplete="off"/>
        <button>Send</button>
    </form>
    <ul id="messages"></ul>
    <script>
        var senderId = {{user_id}};
        var ws = new WebSocket("ws://" + location.host + "/chat/" + senderId);

        ws.onmessage = function(event) {
            var messages = document.getElementById('messages');
            var message = document.createElement('li');
            message.textContent = event.data;
            messages.appendChild(message);
        };

        function sendMessage(event) {
            var receiverId = document.getElementById("receiverId").value;
            var adId = document.getElementById("adId").value;
            var messageText = document.getElementById("messageText").value;

            ws.send(JSON.stringify({
                receiver_id: receiverId,
                advertisement_id: adId,
                message: messageText
            }));

            document.getElementById("messageText").value = '';
            event.preventDefault();
        }
    </script>
</body>
</html>
"""

@router.get("/chat/{user_id}")
async def get_chat_page(user_id: int):
    html = chat_html.replace("{{user_id}}", str(user_id))
    return HTMLResponse(html)

@router.websocket("/chat/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    await websocket.accept()
    active_connections[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_json()
            receiver_id = int(data["receiver_id"])
            ad_id = int(data["advertisement_id"])
            message = data["message"]

            # Check if the receiver owns the advertisement
            ad = db.query(DbAdvertisement).filter_by(id=ad_id, user_id=receiver_id).first()
            if ad and receiver_id in active_connections:
                await active_connections[receiver_id].send_text(
                    f"User {user_id} (ad {ad_id}): {message}"
                )
            # Optionally, you can else send an error or ignore the message
    except WebSocketDisconnect:
        del active_connections[user_id]
        
#end Tina
