export default function TopBar() {
  return (
    <header className="w-full p-4 flex items-center justify-between">
      <img src="/assets/logo.svg" alt="Logo" className="h-10 p1" />
      <h1 className="text-5xl text-red mr-24 text-pink-600">AI Powered Multimodal Meme Search</h1>
      <div className="w-10"></div> {/* Spacer */}
    </header>
  );
}