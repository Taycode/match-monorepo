import React from "react";
import ReactDOM from "react-dom/client";
import App from "./pages/App.tsx";
import "./index.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Search from "./pages/Search.tsx";
import SearchEngine from "./pages/SearchEngine.tsx";
import SignIn from "./pages/SignIn.tsx";
import Posting from "./pages/Posting.tsx";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import PostList from "./pages/PostList.tsx";
import NotFound from "./pages/NotFound.tsx";
import TalentPool from "./pages/TalentPool.tsx";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <ToastContainer />
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/search" element={<Search />} />
        <Route path="/searchengine" element={<SearchEngine />} />
        <Route path="/signin" element={<SignIn />} />
        <Route path="/post" element={<Posting />} />
        <Route path="/post/:id" element={<PostList />} />
        <Route path="/talent-pool" element={<TalentPool />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
