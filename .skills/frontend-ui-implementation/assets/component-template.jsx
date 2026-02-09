import React from "react";

function ComponentTemplate({
    title = "Section title",
    loading = false,
    error = "",
    items = [],
}) {
    if (loading) {
        return <div className="p-4 text-sm text-gray-400">Loading...</div>;
    }

    if (error) {
        return (
            <div className="p-4 rounded border border-red-600 bg-red-950/30 text-red-300 text-sm">
                {error}
            </div>
        );
    }

    return (
        <section className="rounded-xl border border-gray-700 bg-gray-900/60 p-4">
            <h2 className="text-lg font-semibold text-white mb-3">{title}</h2>
            <ul className="space-y-2">
                {items.map((item, idx) => (
                    <li key={idx} className="text-sm text-gray-300">
                        {item}
                    </li>
                ))}
            </ul>
        </section>
    );
}

export default ComponentTemplate;
