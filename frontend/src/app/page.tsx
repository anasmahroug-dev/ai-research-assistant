"use client";

import { useEffect, useState } from "react";

import Sidebar from "@/components/Sidebar";
import ChatWindow from "@/components/ChatWindow";
import PdfSiderbar from "@/components/PdfSidebar";
import MessageContent from "@/components/MessageContent";


import {getConversations,
  getMessages,
  getPdfs,
  createConversation,
  uploadPDF,
  deleteConversation,
  renameConversation,
  sendMessageStream,

} from "@/lib/api";

import dynamic from "next/dynamic";

const PDFViewer = dynamic(
  () => import("@/components/PDFViewer"),
  {
    ssr: false,
  }
);



export default function Home(){
  
  const userId = "consolas";

  const [conversations, setConversations] = useState<any[]>([]);
  const [messages, setMessages] = useState<any[]>([]);
  const [pdfs, setPdfs] = useState<any[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedPdf, setSelectedPdf] = useState<string | null>(null);
  const [selectedPages, setSelectedPages] = useState<number[]>([]);
  
  useEffect(()=>{

    async function loadConversations(){
      const data =
      await getConversations(userId);
      setConversations(data);
    }
    loadConversations();


  }, []);

  async function handleSelectConversation(
    conversation: any
  ){
    setSelectedConversation(conversation);

    const messagesData = await getMessages(conversation.id);

    setMessages(messagesData);

    const pdfsData = 
    await getPdfs(conversation.id);

    setPdfs(pdfsData);

  }

  async function handleSendMessage(text: string){
    let conversation = selectedConversation;
    if (!conversation){
      conversation = await createConversation(userId);
    

    setConversations((prev)=> [conversation, ...prev]);

    setSelectedConversation(conversation);
    }


    const userMessage = {role: "user",
      message:text
    };



    setMessages((prev) => [
      ...prev, userMessage]);

  const botMessage ={
    role: "bot", message: ""
  };


  setMessages((prev) => [...prev, botMessage]);

  await sendMessageStream(conversation.id, text, (chunk) => {
    setMessages((prev) => {
      const updated = [...prev];
      const lastMessage = updated[updated.length -1];
      updated[updated.length -1] = {...lastMessage,
        message: lastMessage.message + chunk
      };
      return updated;
  
  });

  }
);
  
}

  async function handleNewConversation(){
    const newConversation = await createConversation(userId);
    setConversations((prev)=> [
      newConversation,
       ...prev,]);
    
    setSelectedConversation(newConversation);
    
    setMessages([]);
    setPdfs([]);
  }

  async function handleUploadPdf(file: File){
    let conversation = selectedConversation;

    if (!conversation){
      conversation = await createConversation(userId);
      setConversations((prev)=> [conversation, ...prev]);
      setSelectedConversation(conversation);
    }

    await uploadPDF(conversation.id, file);

    const updatedPdfs = await getPdfs(conversation.id);

    setPdfs(updatedPdfs);


  }

  async function handleDeleteConversation(conversationId: number){
    await deleteConversation(conversationId);

    setConversations((prev) => 
      prev.filter(
        (conv)=> conv.id !== conversationId));
    
    if (
      selectedConversation?.id ===
      conversationId
    ) {

      setSelectedConversation(null);
      setMessages([]);
      setPdfs([]);

    }

  }

  async function handleRenameConversation(conversationId: number, title: string){

    const updated = await renameConversation(conversationId, title);

    setConversations((prev)=> 
    prev.map((conv)=>
    conv.id === conversationId
      ? updated
      : conv
      )
    );
  }

  return (
    <main className="flex h-screen bg-zinc-800">
      <Sidebar
      conversations={conversations} 
      onSelectConversation={handleSelectConversation}
      onNewConversation={handleNewConversation}
      onDeleteConversation={handleDeleteConversation}
      onRenameConversation={handleRenameConversation}
      userId= {userId}
      />
      <ChatWindow 
      messages={messages}
      onSend={handleSendMessage}
      onUploadPdf={handleUploadPdf}
      isLoading={isLoading}
      onCitationClick={(filename, pages) => {
        setSelectedPdf(`http://localhost:8000/uploads/${encodeURIComponent(filename)}`);
        setSelectedPages(pages);
      }}
      />
      
      {selectedPdf && (
        <PDFViewer 
         fileUrl={selectedPdf}
          pages={selectedPages}
          onClose={()=> setSelectedPdf(null)}
        />
          )}

      <PdfSiderbar
      pdfs={pdfs} />

    </main>
  );

}