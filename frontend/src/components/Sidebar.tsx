 import { useState } from "react";
 import {Pencil, Trash2, UserIcon, Plus, ChevronUp, User, Settings, LogOut} from "lucide-react";
 import ConfirmDialog from "./ConfirmDialog"
 
 type Props = {
    conversations: any[];
    onSelectConversation: (conv: any) => void;
    onNewConversation:() => void;
    onDeleteConversation: (id: number) => void;
    onRenameConversation: (id:number, title: string) => void;
    username: string;
    onLogout:() => void;
    
  }

export default function Sidebar({conversations, onSelectConversation,onNewConversation,onDeleteConversation, onRenameConversation, username, onLogout}: Props) {
  const [editingId, setEditingId] =
  useState<number | null>(null);

  const [editTitle, setEditTitle] = 
  useState("");

  const [conversationToDelete, setConversationToDelete] =
  useState<number | null>(null);

  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <aside className="w-72 h-screen bg-zinc-900 text-white p-4 flex flex-col">

      <button
        onClick={onNewConversation}

        className="flex items-center gap-2 mb-4 bg-white text-black p-3 rounded-xl cursor-pointer font-medium hover:bg-zinc-200"
      >
        <Plus size={16}/> New Chat
        
      </button>

      <h2 className="text-xl font-bold mb-4">
        Conversations
      </h2>

      <div className="flex-1 overflow-y-auto space-y-2 pr-1">
        {conversations.map((conv) => (
          <div
            key={conv.id}

            onClick={()=>
              onSelectConversation(conv)
            }

            className="group w-full text-left p-3 rounded-lg cursor-pointer bg-zinc-800 hover:bg-zinc-700"
          >
            <div className ="flex items-center justify-between">
              {editingId === conv.id ? (

                <input value={editTitle}
                onChange={(e) =>
                  setEditTitle(e.target.value)
                }
                onKeyDown={async(e)=> {
                  if (e.key === "Enter"){
                    await onRenameConversation(conv.id, editTitle);
                    setEditingId(null);
                  }
                  if (e.key ==="Escape"){
                    setEditingId(null);
                  }
                }}
                autoFocus

                className="bg-zinc-700 text-white px-2 py-1 rounded w-full"
                />

              ) : (
                <>
                  <span className="truncate">
                    {conv.title}
                  </span>
                <div
                className="hidden group-hover:flex items-center gap-2"
                >
                  <button
                  onClick={(e)=>{
                    e.stopPropagation();
                    setEditingId(conv.id);
                    setEditTitle(conv.title);
                  }}
                  className="cursor-pointer
                  hover:bg-zinc-800
                  rounded-lg"
                  ><Pencil size={16}/></button>

                  <button 
                  onClick={(e) => {
                    e.stopPropagation();
                    setConversationToDelete(conv.id);
                    
                  }}
                  className="cursor-pointer
                  hover:bg-zinc-800
                  rounded-lg"  
                  ><Trash2 size={16}/></button>

                </div>
                </>
              )
              }
              </div>
          </div>
        ))}
      </div>

      <div className="relative mt-4">

  <button
    onClick={() => setMenuOpen(!menuOpen)}
    className="flex w-full items-center justify-between rounded-xl bg-zinc-800 hover:bg-zinc-700 p-3 transition cursor-pointer"
  >
    <div className="flex items-center gap-3">
      <UserIcon size={22} />
      <span>{username}</span>
    </div>

    <ChevronUp
    size={18}
    className={`transition-transform duration-200 ${
    menuOpen ? "rotate-180" : ""
    }`}
    />
  </button>

  {menuOpen && (
    <div className="absolute bottom-full mb-2 w-full rounded-xl bg-zinc-800 border border-zinc-700 shadow-lg overflow-hidden">
      {/*
      <button
        className="flex w-full items-center gap-3 px-4 py-3 hover:bg-zinc-700 transition cursor-pointer"
      >
        <Settings size={18} />
        Settings
      </button>

      <button
        className="flex w-full items-center gap-3 px-4 py-3 hover:bg-zinc-700 transition cursor-pointer"
      >
        <UserIcon size={18} />
        Profile
      </button>

      */}
      <div className="border-t border-zinc-700" />

      <button
        onClick={onLogout}
        className="flex w-full items-center gap-3 px-4 py-3 text-red-400 hover:bg-zinc-700 hover:text-red-300 transition cursor-pointer"
      >
        <LogOut size={18} />
        Logout
      </button>

    </div>
  )}

</div>
        <ConfirmDialog
        open={conversationToDelete !== null}
        title="Delete conversation?"
        message="This will permanently delete this conversation and all of its messages."
        confirmText="Delete"
        cancelText="Cancel"
        onCancel={() => setConversationToDelete(null)}
        onConfirm={() => {
          if (conversationToDelete !== null) {
            onDeleteConversation(conversationToDelete);
            setConversationToDelete(null);
          }
        }}
      />
    </aside>
  );
}