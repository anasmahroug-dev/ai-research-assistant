 import { useState } from "react";
 import {Pencil, Trash2, UserIcon, Plus} from "lucide-react";
 
 type Props = {
    conversations: any[];
    onSelectConversation: (conv: any) => void;
    onNewConversation:() => void;
    onDeleteConversation: (id: number) => void;
    onRenameConversation: (id:number, title: string) => void;
    userId: string;
    
  }




export default function Sidebar({conversations, onSelectConversation,onNewConversation,onDeleteConversation, onRenameConversation, userId}: Props) {
  const [editingId, setEditingId] =
useState<number | null>(null);

const [editTitle, setEditTitle] = 
useState("");
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

                    const confirmed =
                    confirm("Delete conversation?");

                    if (confirmed){
                      onDeleteConversation(conv.id);

                    }
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

      <button
        className="flex items-center gap-5 mt-4 bg-zinc-800 hover:bg-zinc-700 p-3 rounded-xl cursor-pointer text-left">
       <UserIcon size={32}/>{userId}
      </button>

    </aside>
  );
}