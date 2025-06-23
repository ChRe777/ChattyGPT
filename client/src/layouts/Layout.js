// Styles
//
import "./Layout.css"

// Used Components
//
import ChatInput from "components/ChatInput";
import Navbar from "components/Navbar";


// Component
//
function Layout({ children }) {

    // Body
    //
    return (

        <div className="app-layout">
            <div className="header stick-top px-2">
                <Navbar />
            </div>
            <main className="main">
                {children}
            </main>
            <footer className="footer">
                <ChatInput />
            </footer>
        </div>


    );
}

export default Layout;
