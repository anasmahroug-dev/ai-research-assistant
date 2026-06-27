export default function Sidebar(){

    const conversations = [
        "Conversation Ia",
        "Gestion de projet",
        "Maths et physiques"
    ];

    return (<aside className="w-72 bg-zinc-900 text-white p-4">
        <h2 className="text-xl font-bold mb-4">
            Conversations
        </h2>

           <button
        className="mb-4 bg-white text-black p-3 rounded-xl font-medium hover:bg-zinc-300"
      >
        + New Chat
      </button>

        <div className="space-y-2">
            {conversations.map((conv, index) => (
                <button
                key ={index}
                className="w-full text-left p-3 rounded-lg bg-zinc-800 hover:bg-zinc-700"
                >{conv}</button>
            ))}

        </div>
    </aside>)

}