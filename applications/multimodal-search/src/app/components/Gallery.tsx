"use client";

import { ReactElement } from "react";

export default function Gallery({ imgs }: { imgs: Array<string> }) {
  const imgList: Array<ReactElement> = [];
  imgs.map((img, i) => {
    imgList.push(
      <div className={"w-1/4 md:p-2"}>
        <img
          alt="gallery"
          className="block h-full w-full rounded-lg object-cover object-center"
          src={img}
        />
      </div>
    );
  });

  return (
    <div className="container mx-auto px-5 lg:px-32 lg:pt-24 flex flex-wrap">
      {imgList}
    </div>
  );
}
