// FlowBuilder MVP – React + Tailwind (bloques dinámicos con color de tipo, drag & drop y ejecución encadenada)
"use client";

import { useState } from "react";
import { DndContext, closestCenter } from "@dnd-kit/core";
import {
  SortableContext,
  verticalListSortingStrategy,
  useSortable,
  arrayMove,
} from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";

const TYPE_COLORS: Record<string, string> = {
  text: "bg-yellow-100 border-yellow-400",
  gancho: "bg-purple-100 border-purple-400",
  audio: "bg-blue-100 border-blue-400",
  image: "bg-green-100 border-green-400",
  longtext: "bg-pink-100 border-pink-400",
};

const TYPE_CIRCLES: Record<string, string> = {
  text: "bg-red-500",
  gancho: "bg-purple-500",
  audio: "bg-blue-500",
  image: "bg-green-500",
  longtext: "bg-pink-500",
};
const TYPE_ICONS: Record<string, string> = {
  text: "📝",
  gancho: "🎯",
  audio: "🔊",
  image: "🖼️",
  longtext: "📄",
};


const MODULES = [
  { id: "gancho", name: "GanchoExpress", input: "text", output: "gancho", endpoint: "/gancho" },
  { id: "voz", name: "VozPremium", input: "text", output: "audio", endpoint: "/voz" },
  { id: "imagen", name: "VisualizerIA", input: "text", output: "image", endpoint: "/imagen" },
  { id: "post", name: "PostMultiplicador", input: "gancho", output: "longtext", endpoint: "/post" },
];

function SortableItem({ id, onRemove }: { id: string; onRemove: () => void }) {
  const mod = MODULES.find((m) => m.id === id);
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
  } = useSortable({ id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  if (!mod) return null;

  return (
    <div
      ref={setNodeRef}
      {...attributes}
      {...listeners}
      style={style}
      className={`p-2 rounded shadow border relative ${TYPE_COLORS[mod.output]} space-y-1`}
    >
      <div className="flex justify-between items-center text-sm">
        <span>{TYPE_ICONS[mod.input]} ➝ {TYPE_ICONS[mod.output]}</span>
        <button onClick={onRemove} className="text-red-500 text-xs">✕</button>
      </div>
      <div className="font-medium">{mod.name}</div>
      <div className="text-xs italic">({mod.input} ➝ {mod.output})</div>
    </div>
  );
}



export default function FlowBuilder() {
  const [inputText, setInputText] = useState("");
  const [flow, setFlow] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const addToFlow = (moduleId: string) => {
    setFlow([...flow, moduleId]);
  };

  const removeFromFlow = (index: number) => {
    const newFlow = [...flow];
    newFlow.splice(index, 1);
    setFlow(newFlow);
  };

  const validateFlow = () => {
    let currentOutput = "text";
    for (const moduleId of flow) {
      const module = MODULES.find((m) => m.id === moduleId);
      if (!module || module.input !== currentOutput) return false;
      currentOutput = module.output;
    }
    return true;
  };

  const executeFlow = async () => {
    setLoading(true);
    let data: any = inputText;

    try {
      for (const moduleId of flow) {
        const module = MODULES.find((m) => m.id === moduleId);
        if (!module) continue;

        const res = await fetch(`http://localhost:8000${module.endpoint}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ texto: data, texto_principal: data, input: data }),
        });

        const json = await res.json();
        data = json.output || json.result || json.transcript || JSON.stringify(json);
      }
      setResult(data);
    } catch (err) {
      console.error("Error al ejecutar flujo:", err);
      setResult("❌ Error durante la ejecución del flujo");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="max-w-2xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">🧠 IA Flow Builder</h1>

      <div className="space-y-2">
        <label className="block font-medium">📝 Input inicial:</label>
        <input
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="¿Sobre qué quieres generar contenido?"
          className="w-full border p-2 rounded"
        />
      </div>

      <div className="space-y-2">
        <p className="font-medium">🧩 Agrega módulos al flujo:</p>
        <div className="flex gap-2 flex-wrap">
        {MODULES.map((m) => (
          <button
            key={m.id}
            onClick={() => addToFlow(m.id)}
            className={`px-3 py-1 rounded text-sm border ${TYPE_COLORS[m.output]} flex items-center gap-2`}
          >
            <span>{TYPE_ICONS[m.input]}</span>
            <span className="font-medium">{m.name}</span>
            <span>{TYPE_ICONS[m.output]}</span>
          </button>
        ))}

        </div>
      </div>

      <div className="space-y-2">
        <p className="font-medium">🧪 Tu flujo actual (puedes reordenar):</p>

        <DndContext
          collisionDetection={closestCenter}
          onDragEnd={(event) => {
            const { active, over } = event;
            if (active.id !== over?.id) {
              const oldIndex = flow.indexOf(active.id as string);
              const newIndex = flow.indexOf(over?.id as string);
              setFlow(arrayMove(flow, oldIndex, newIndex));
            }
          }}
        >
          <SortableContext items={flow} strategy={verticalListSortingStrategy}>
            <div className="flex flex-col gap-2">
              {flow.map((moduleId, index) => (
                <SortableItem
                  key={moduleId + index}
                  id={moduleId}
                  onRemove={() => removeFromFlow(index)}
                />
              ))}
            </div>
          </SortableContext>
        </DndContext>

        {!validateFlow() && (
          <p className="text-red-600 text-sm">❌ El flujo no es válido (incompatibilidad de entrada/salida)</p>
        )}
      </div>

      <button
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:opacity-40"
        disabled={!inputText || !validateFlow() || loading}
        onClick={executeFlow}
      >
        🚀 Ejecutar flujo
      </button>

      {loading && <p className="text-sm text-blue-600">Procesando...</p>}
      {result && (
        <div className="mt-4 p-4 bg-gray-100 rounded border">
          <h2 className="font-medium mb-2">Resultado final:</h2>
          <pre className="whitespace-pre-wrap text-sm">{result}</pre>
        </div>
      )}
    </main>
  );
}
