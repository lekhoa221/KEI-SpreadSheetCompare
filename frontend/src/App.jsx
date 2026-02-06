import React, { useState } from 'react';
import UploadZone from './components/UploadZone.jsx';
import SxSView from './components/SxSView.jsx';

function App() {
    const [comparisonResult, setComparisonResult] = useState(null);

    return (
        <div className="min-h-screen bg-gray-900 text-white font-sans selection:bg-purple-500 selection:text-white">
            {/* Header */}
            <header className="border-b border-gray-800 bg-gray-900/50 backdrop-blur sticky top-0 z-10">
                <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center font-bold text-lg">S</div>
                        <h1 className="text-xl font-bold tracking-tight">Spreadsheet Compare <span className="text-purple-400 font-normal">AI</span></h1>
                    </div>
                    <div className="text-sm text-gray-400">v0.1.0 Beta</div>
                </div>
            </header>

            {/* Main Content */}
            <main className="container mx-auto px-4 py-12">
                {!comparisonResult ? (
                    <div className="fade-in">
                        <div className="text-center mb-12">
                            <h1 className="text-4xl md:text-5xl font-extrabold mb-6 bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                                Comparing Excel Files <br /> Made Intelligent.
                            </h1>
                            <p className="text-lg text-gray-400 max-w-2xl mx-auto leading-relaxed">
                                Upload two spreadsheets to instantly detect changes in values, formulas, and structure.
                                Powered by local AI for deep insights.
                            </p>
                        </div>

                        <UploadZone onCompareResult={setComparisonResult} />
                    </div>
                ) : (
                    <SxSView
                        files={comparisonResult.files}
                        comparisonData={comparisonResult.data}
                        onBack={() => setComparisonResult(null)}
                    />
                )}
            </main>
        </div>
    )
}

export default App;
