"use client";

import { useEffect, useState } from "react";

import Sidebar from "@/components/Sidebar";
import ChatWindow from "@/components/ChatWindow";
import PdfSiderbar from "@/components/PdfSidebar";

import {getConversations,
  getMessages,
  getPdfs,
  sendMessage,
  createConversation,
  uploadPDF,
  deleteConversation,
  renameConversation,

} from "@/lib/api";



export default function Home(){
  
  const userId = "consolas";

  const [conversations, setConversations] = useState<any[]>([]);
  const [messages, setMessages] = useState<any[]>([]);
  const [pdfs, setPdfs] = useState<any[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  
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

    setIsLoading(true);
    
  
  const data = await sendMessage(conversation.id, text);

  setIsLoading(false);
  
  const botMessage ={
    role: "bot", message: data.response,
  };

  setMessages((prev) => [...prev, botMessage]);

  }

  async function handleNewConversation(){
    const newConversation = await createConversation(userId);
    setConversations((prev)=> [
      newConversation,
       ...prev,]);
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
      />
      <PdfSiderbar
      pdfs={pdfs} />

    </main>
  );



}