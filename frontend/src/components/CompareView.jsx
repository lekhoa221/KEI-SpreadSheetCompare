import React, { useState } from 'react';
import axios from 'axios';
import { ArrowLeft, CheckCircle, AlertTriangle, BarChart3, Bot, Sparkles } from 'lucide-react';

const CompareView = ({ result, onReset }) => {
    const { summary, changes } = result;
    const [analysis, setAnalysis] = useState(null);
    const [analyzing, setAnalyzing] = useState(false);

    const handleAnalyze = async () => {
        setAnalyzing(true);
        try {
            const res = await axios.post('/api/analyze', { summary, changes });
            setAnalysis(res.data.analysis);
        } catch (error) {
            console.error("AI Analysis failed", error);
            setAnalysis("Could not generate analysis. Ensure Ollama is running.");
        } finally {
            setAnalyzing(false);
        }
    };

    return (
        <div className="w-full max-w-6xl mx-auto p-4 animate-fade-in">
            <button
                onClick={onReset}
                className="flex items-center gap-2 text-gray-400 hover:text-white mb-6 transition-colors"
            >
                <ArrowLeft className="w-4 h-4" /> Back to Upload
            </button>

            {/* Summary Dashboard */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-lg">
                    <div className="flex items-center justify-between mb-2">
                        <h3 className="text-gray-400 text-sm font-medium">Total Changes</h3>
                        <BarChart3 className="w-5 h-5 text-blue-400" />
                    </div>
                    <p className="text-3xl font-bold text-white">{summary.changes_count}</p>
                </div>

                <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-lg">
                    <div className="flex items-center justify-between mb-2">
                        <h3 className="text-gray-400 text-sm font-medium">Rows Scanned</h3>
                        <CheckCircle className="w-5 h-5 text-green-400" />
                    </div>
                    <p className="text-3xl font-bold text-white">{summary.total_rows}</p>
                </div>

                <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-lg">
                    <div className="flex items-center justify-between mb-2">
                        <h3 className="text-gray-400 text-sm font-medium">Columns Scanned</h3>
                        <AlertTriangle className="w-5 h-5 text-yellow-400" />
                    </div>
                    <p className="text-3xl font-bold text-white">{summary.total_cols}</p>
                </div>
            </div>

            {/* AI Analysis Section */}
            <div className="mb-8 bg-gradient-to-br from-indigo-900/50 to-purple-900/50 p-6 rounded-xl border border-indigo-500/30">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-xl font-semibold text-white flex items-center gap-2">
                        <Bot className="w-6 h-6 text-purple-400" /> AI Insights
                    </h2>
                    {!analysis && !analyzing && (
                        <button
                            onClick={handleAnalyze}
                            className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-lg transition-all shadow-lg hover:shadow-purple-500/20"
                        >
                            <Sparkles className="w-4 h-4" /> Analyze with AI
                        </button>
                    )}
                </div>

                {analyzing && (
                    <div className="text-gray-300 animate-pulse flex items-center gap-2">
                        <Sparkles className="w-4 h-4 text-yellow-400 animate-spin" />
                        Reading data and generating insights...
                    </div>
                )}

                {analysis && (
                    <div className="prose prose-invert max-w-none text-gray-200">
                        <p className="whitespace-pre-line leading-relaxed">{analysis}</p>
                    </div>
                )}
            </div>

            {/* Changes Table */}
            <div className="bg-gray-800 rounded-xl border border-gray-700 shadow-xl overflow-hidden">
                <div className="p-4 border-b border-gray-700 bg-gray-800/50 backdrop-blur">
                    <h3 className="text-lg font-semibold text-white">Detailed Differences</h3>
                </div>

                {changes.length === 0 ? (
                    <div className="p-12 text-center text-gray-400">
                        <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-4" />
                        <p className="text-lg text-white">No differences found!</p>
                        <p>The files are identical.</p>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm text-left">
                            <thead className="text-xs text-gray-400 uppercase bg-gray-900/50">
                                <tr>
                                    <th className="px-6 py-3">Row</th>
                                    <th className="px-6 py-3">Column</th>
                                    <th className="px-6 py-3 text-red-300">Original Value</th>
                                    <th className="px-6 py-3 text-green-300">New Value</th>
                                    <th className="px-6 py-3">Type</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-700">
                                {changes.map((change, index) => (
                                    <tr key={index} className="bg-gray-800 hover:bg-gray-750 transition-colors">
                                        <td className="px-6 py-4 font-medium text-gray-300">{change.row + 1}</td>
                                        <td className="px-6 py-4 font-mono text-blue-300">{change.col}</td>
                                        <td className="px-6 py-4 text-red-400 bg-red-900/10 font-mono">
                                            {change.old || <span className="text-gray-600 italic">(empty)</span>}
                                        </td>
                                        <td className="px-6 py-4 text-green-400 bg-green-900/10 font-mono">
                                            {change.new || <span className="text-gray-600 italic">(empty)</span>}
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className="px-2 py-1 text-xs font-semibold rounded-full bg-yellow-900/30 text-yellow-500 border border-yellow-800">
                                                {change.type}
                                            </span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
};

export default CompareView;
