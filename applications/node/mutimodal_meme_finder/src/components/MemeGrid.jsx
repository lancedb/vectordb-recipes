import MemeCard from "./MemeCard";

export default function MemeGrid({ memes, error }) {

  if (error) {
    return <p className="text-red-00 mt-8 text-center">{error}</p>;
  }

  return (
    <div className="w-full p-4 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {memes.length === 0 ? (
        <p className="text-center col-span-full text-gray-400">
          Hey there, ready to find some hilarious memes?
        </p>
      ) : (
         memes.map((meme, index) => <MemeCard key={index} meme={meme}/>)
      )}
    </div>
  );
}
