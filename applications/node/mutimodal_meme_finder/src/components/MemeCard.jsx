import { DownloadSimple} from "phosphor-react";

export default function MemeCard({ key,meme }) {
  return (
    <div className="p-3 rounded-lg shadow-lg transition-transform hover:scale-105 shadow-gray-500">
      <img src={meme} alt="Meme" className="w-full rounded-lg h-96" />
      <a
        href={meme}
        download
        className="block bg-red-400 text-white text-center py-2 mt-2 rounded-lg hover:bg-pink-600 transition flex items-center justify-center"
      >
        <DownloadSimple size={32} />
        <span className="ml-4">Download</span>
      </a>
    </div>
  );
}
