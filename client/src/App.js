import "./App.css";

// Components
//
import Layout from "layouts/Layout";
import ChatMessages from "components/ChatMessages";
import ChatMessagesSubscriber from "components/ChatMessageSubscriber";
import TreeView from "components/TreeView";
import Breadcrumb from "components/BreadCrumb";

// Example data
//
const data = [
    {
        id: 1,
        label: "Fruits",
        children: [
            { id: 2, label: "Apple" },
            {
                id: 3,
                label: "Banana",
                children: [
                    { id: 7, label: "with Milk" },
                    { id: 8, label: "Brown jjj" },
                ],
            },
        ],
    },
    {
        id: 4,
        label: "Vegetables",
        children: [
            { id: 5, label: "Carrot" },
            { id: 6, label: "Broccoli" },
        ],
    },
];

// Component
//
function App() {
    return (
        <Layout>
            <Breadcrumb />
            <TreeView data={data} />
            <ChatMessages />
            <ChatMessagesSubscriber />
        </Layout>
    );
}

export default App;
