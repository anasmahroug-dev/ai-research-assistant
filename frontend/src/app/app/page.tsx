"use client";

import { useEffect, useState } from "react";

import Sidebar from "@/components/Sidebar";
import ChatWindow from "@/components/ChatWindow";
import PdfSidebar from "@/components/PdfSidebar";
import MessageContent from "@/components/MessageContent";


import {getConversations,
  getMessages,
  getPdfs,
  createConversation,
  uploadPDF,
  deleteConversation,
  renameConversation,
  sendMessageStream,
  getChunk,
  deletePdf,

} from "@/lib/api";

import {getCurrentUser, logout} from "@/lib/auth";
import {useRouter} from "next/navigation";

import dynamic from "next/dynamic";

const PDFViewer = dynamic(
  () => import("@/components/PDFViewer"),
  {
    ssr: false,
  }
);


export default function Home(){
  
  const [conversations, setConversations] = useState<any[]>([]);
  const [messages, setMessages] = useState<any[]>([]);
  const [pdfs, setPdfs] = useState<any[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedPdf, setSelectedPdf] = useState<string | null>(null);
  const [selectedPages, setSelectedPages] = useState<number[]>([]);
  const [selectedChunkId, setSelectedChunkId] = useState<number | null>(null);
  const [highlightChunk, setHighlightChunk] = useState("");
  const [isUploadingPdf, setIsUploadingPdf] = useState(false);
  const [user, setUser] = useState<any>(null);
  const router = useRouter();
  
  useEffect(()=> {
    async function loadUser(){
      
      const currentUser = await getCurrentUser();

      if (!currentUser){
        window.location.href = "/login";
        return;
      }

      setUser(currentUser);

    }

    loadUser();
  }, []);
  
  
  useEffect(()=>{

    if (!user) return;

    async function loadConversations(){
      const data =
      await getConversations();
      setConversations(data);
    }
    loadConversations();


  }, [user]);

  function handleLogout(){
  logout();
  router.push("/");
}

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
      conversation = await createConversation();
    

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

  await sendMessageStream(
    conversation.id,
    text,
    (event) => {

        switch (event.type) {

            case "token":

                setMessages(prev => {

                    const updated = [...prev];

                    const lastMessage =
                        updated[updated.length - 1];

                    updated[updated.length - 1] = {
                        ...lastMessage,
                        message: lastMessage.message + event.data,
                    };

                    return updated;
                });

                break;

            case "update":

                setMessages(prev => {

                    const updated = [...prev];

                    const lastMessage =
                        updated[updated.length - 1];

                    updated[updated.length - 1] = {
                        ...lastMessage,
                        message: event.data,
                    };

                    return updated;
                });

                break;

            case "done":

                break;
        }

    }
);
  
}

  async function handleNewConversation(){
    const newConversation = await createConversation();
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
      conversation = await createConversation();
      setConversations((prev)=> [conversation, ...prev]);
      setSelectedConversation(conversation);
    }

    setIsUploadingPdf(true);

    try{

      await uploadPDF(conversation.id, file);

      const updatedPdfs = await getPdfs(conversation.id);

      setPdfs(updatedPdfs);
    } finally{
      setIsUploadingPdf(false);
    }
    
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

  async function handleDeletePdf(pdfId:number){
    await deletePdf(pdfId);
    setPdfs(prev => 
      prev.filter(pdf => pdf.id !== pdfId)
    )
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
    
    <main className="flex h-screen overflow-hidden bg-zinc-800">
        
      <Sidebar
      conversations={conversations} 
      onSelectConversation={handleSelectConversation}
      onNewConversation={handleNewConversation}
      onDeleteConversation={handleDeleteConversation}
      onRenameConversation={handleRenameConversation}
      username= {user?.username ?? ""}
      onLogout={handleLogout}
      />
       <div className="flex flex-col flex-1 min-w-0 overflow-hidden">
         {user?.is_guest && (
        <div className="flex items-center justify-between rounded-xl border border-zinc-700 bg-zinc-900 px-6 py-3">
          <div>
            <p className="font-medium text-white">
              You're using a guest account
            </p>
            <p className="text-sm text-zinc-400">
              Create a free account to save your chats and uploaded PDFs permanently.
            </p>
          </div>

          <button
            onClick={() => router.push("/register")}
            className="rounded-lg bg-white px-4 py-2 text-black font-medium hover:bg-zinc-200 transition"
          >
            Create Account
          </button>
        </div>
      )}
      <ChatWindow 
      className="flex-1"
      messages={messages}
      onSend={handleSendMessage}
      onUploadPdf={handleUploadPdf}
      isLoading={isLoading}
      onCitationClick={async (filename, pages, chunkId) => {
        const chunk = await getChunk(chunkId)
        const keywords = chunk.text
        setSelectedPdf(`http://localhost:8000/uploads/${encodeURIComponent(filename)}`);
        setSelectedPages(pages);
        setSelectedChunkId(chunkId);
        setHighlightChunk(chunk.text);

      }}
      />
      </div>
      
      {selectedPdf && (
        <PDFViewer 
         fileUrl={selectedPdf}
          pages={selectedPages}
          highlightChunk={highlightChunk}
          onClose={()=> setSelectedPdf(null)}
        />
          )}

      <PdfSidebar
      pdfs={pdfs} 
      isUploading={isUploadingPdf}
      onDeletePdf={handleDeletePdf}/>

    </main>
  );

}