import './App.css';

function App() {
    return (
        <div className="App flex items-center justify-center min-h-full min-w-full bg-background-color">
            <header className="App-header">
                <link rel="preconnect" href="https://fonts.gstatic.com"/>
                <link href="https://fonts.googleapis.com/css2?family=Major+Mono+Display&display=swap" rel="stylesheet"/>
                <h1 className="text-9xl font-title">Abiogenesis.</h1>
                <a
                    className="text-secondary-color"
                    href="/recycle"
                    target=""
                    rel="noopener noreferrer"
                >
                    Start webapp
                </a>
            </header>
        </div>
    );
}

export default App;
