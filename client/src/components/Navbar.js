// Store
//
import useChatMessageStore from "stores/chatMessageStore";

function Navbar() {
    const { foundDocuments } = useChatMessageStore();

    return (
        <header className="navbar py-2">
            <section className="navbar-section">
                <a
                    href="https://github.com/ChRe777/ChattyGPT"
                    className="text-bold mr-2"
                >
                    ChattyGPT
                </a>
                <a
                    href="https://github.com/ChRe777/ChattyGPT"
                    className="btn btn-link"
                >
                    Docs
                </a>
                <a
                    href="https://github.com/ChRe777/ChattyGPT"
                    className="btn btn-link"
                >
                    GitHub
                </a>
            </section>
            <section className="navbar-section">
                {foundDocuments > 0 && (
                    <span className="mr-2 badge" data-badge={foundDocuments}>
                        Found Docs
                    </span>
                )}
                <button className="btn btn-primary btn-sm" disabled>
                    Anmelden
                </button>
                <div className="mx-2"></div>
            </section>
        </header>
    );
}

export default Navbar;
