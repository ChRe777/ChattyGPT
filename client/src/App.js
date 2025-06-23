import './App.css';

// Components
//
import Layout from 'layouts/Layout';
import ChatMessages from 'components/ChatMessages';
import ChatMessagesSubscriber from 'components/ChatMessageSubscriber';

// Component
//
function App() {
    return (
        <Layout>
            <ChatMessages />
            <ChatMessagesSubscriber />
        </Layout>
    );
}

export default App;
