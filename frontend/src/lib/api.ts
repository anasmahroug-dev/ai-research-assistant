import { APP_DIR_ALIAS } from "next/dist/lib/constants";

const API_URL = "http://localhost:8000";

export async function getConversations(userId: string)
{
    const response = await fetch(
        `${API_URL}/conversations/${userId}`

    );
    return response.json();
}

export async function createConversation(userId: string){
    const response = await fetch(
        `${API_URL}/conversations/?user_id=${userId}`,
        {
            method: "POST",
        }
    );
    return response.json();
}

export async function getMessages(conversationId: number){
    const response = await fetch(
        `${API_URL}/chat/history/${conversationId}`
    );
    return response.json();
}



export async function sendMessageStream(conversationId: number, message: string, 
    onChunk: (chunk: string)=> void){

        const response = await fetch(
            `${API_URL}/chat/`,
            {
                method: "POST",
                headers:{
                    "Content-Type": "application/json",
                },

                body: JSON.stringify({conversation_id: conversationId,
                    message,}),


            }
        );

        const reader = response.body?.getReader();

        if (!reader) return;
        const decoder = new TextDecoder();
        while (true){
            const { done, value } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value);
            onChunk(chunk);
        }

}




export async function uploadPDF(conversationId: number, file: File){

    const formData = new FormData();

    formData.append("conversation_id", String(conversationId));

    formData.append("file", file);

    const response= await fetch(
        `${API_URL}/pdf/upload`,
        {
            method: "POST",
            body: formData,
        }
    );
    return response.json();
}

export async function getPdfs(conversationId: number) {

  const response = await fetch(
    `${API_URL}/pdf/${conversationId}`
  );

  return response.json();
}

export async function deleteConversation(conversationId: number){

    const response = await fetch(
        `${API_URL}/conversations/${conversationId}`,
        {
            method: "DELETE",
        }
    );
    return response.json();

}

export async function renameConversation(conversationId: number, title: string){
    const response = await fetch(
        `${API_URL}/conversations/${conversationId}?title=${encodeURIComponent(title)}`,
        {
            method: "PUT",
        }
    );

    return response.json();


}