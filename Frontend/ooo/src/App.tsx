import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./containers/Login/Login";
import Home from "./containers/Home/Home";
import Closet from "./containers/Closet/Closet";
import Outfit from "./containers/Outfit/Outfit";
import OutfitDetail from "./containers/OutfitDetail/OutfitDetail";
import Redirect from "./containers/Redirect/Redirect";

function App() {
	return (
		<BrowserRouter>
			<div className="App">
				<Routes>
					<Route path="/closet" element={<Closet title={"Closet"} />} />
					<Route path="/home" element={<Home />} />
					<Route path="/outfit" element={<Outfit />} />
					<Route path="/outfit/:id" element={<OutfitDetail />} />
					<Route path="/" element={<Login />} />
					<Route path="*" element={<h1>Not Found</h1>} />
					<Route path="/Redirect" element={<Redirect />} />
				</Routes>
			</div>
		</BrowserRouter>
	);
}

export default App;
