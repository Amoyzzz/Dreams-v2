import Navbar from "~/components/Navbar";

export default function Index() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow flex flex-col justify-center items-center bg-gray-100">
        <h1 className="text-4xl font-bold text-gray-800">Welcome to DreamsV2</h1>
        <p className="mt-4 text-gray-600">This is a simple single-page website built with Remix and Tailwind CSS.</p>
      </main>
    </div>
  );
}
