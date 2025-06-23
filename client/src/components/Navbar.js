// Store
//
//import useChatMessageStore from 'stores/chatMessageStore';


function Navbar() {

    return (
        <header className="navbar py-2">
            <section className="navbar-section">
                <a href="..." className="text-bold mr-2">ChattyGPT</a>
                <a href="..." className="btn btn-link">Docs</a>
                <a href="..." className="btn btn-link">GitHub</a>
            </section>
            <section className="navbar-section">
                <button className="btn btn-primary btn-sm">Anmelden</button>
                <div className="mx-2"></div>
            </section>
        </header >
    )
}

export default Navbar;
