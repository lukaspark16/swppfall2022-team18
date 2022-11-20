import { logoutUser } from "../../api/user";
import React, { useEffect, useState, useCallback, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import Header from "../../components/Header/Header";
import ClosetItem from "../../components/ClosetItem/ClosetItem";
import "./Home.css";
import OutfitPreview from "../../components/OutfitPreview/OutfitPreview";
import { AppDispatch } from "../../store";
import { selectUserCloth } from "../../store/slices/userCloth";
import { selectOutfit } from "../../store/slices/outfit";
import { fetchUserClothes } from "../../store/slices/userCloth";
import { fetchOutfits } from "../../store/slices/outfit";
import { fetchRecommendOutfit } from "../../store/slices/userCloth";

export default function Home() {
	const navigate = useNavigate();
	const dispatch = useDispatch<AppDispatch>();
	const userClothes = useSelector(selectUserCloth);
	const outfit = useSelector(selectOutfit);
	const [Loading, setLoading] = useState(false);

	//for logout
	const [isSending, setIsSending] = useState(false)
	const checkLoginned = () => {
		console.log("start")
		console.log(localStorage.getItem("username"));
		if(localStorage.getItem("username") !== null){
			return true
		}
		else return false
	};

	useEffect(() => {
		const redirect = () => {
			if (!checkLoginned()) {
				navigate("/");
			}
		};
		redirect();
	}, [isSending]);


	
	useEffect(()=>{
	//closet list, outfitlist 받아오는 것
		const getData = async() => {
			setLoading(true)
			dispatch(fetchUserClothes())
			dispatch(fetchOutfits());
			dispatch(fetchRecommendOutfit());
			setLoading(false)
		}
		getData()
	},[])


	if (Loading) {
		return <div>Loading..</div>;
	} else {
		return (
			<div className="Home">
				<div className="Home-header"
					data-testid='Header'>
					<Header
						clickInfoHandler={() => {
							navigate("/");
						}}
						clickLogoutHandler={async() => {
							await logoutUser().catch((error) => console.log(error))
							setIsSending(!isSending)
						}}
						clickHeaderHandler={() => {
							navigate("/home");
						}}
					></Header>
				</div>

				<div className="HomeTop">
					<div className="ClosetDiv">
						<text id="Closet-text">Closet</text>
						<div className="Closet-image">
							<div className="Closet-item-box"
							data-testid='ClosetItem'>
								{userClothes.userClothes.map((cloth, index) => {
									return(
										<ClosetItem
										key={index}
										source_url={cloth.image_id.toString()} //나중에 바꿔야함.
										type={cloth.type}
										color={cloth.color}
										pattern={cloth.pattern}
										/>
									)
								})}
							</div>
						</div>
						<div className="Closet-button">
							<button
								id="more-button"
								data-testid='more-btn'
								onClick={() => {
									navigate("/closet");
								}}
							>
								More
							</button>
						</div>
					</div>
					<div className="CenterDiv"></div>
					<div className="TodayOutfit"
					data-testid='TodayOutfit'>
						<text id="TodayOutfit-text">Today{"'"}s Outfit</text>
						<div className="TodayOutfit-content">
							{
								userClothes.recommendOutfit !== null ? 
								<div>
									<div className="TodayOutfit-image" >
										<img id="today-outfit-img" src={userClothes.recommendOutfit.image_id.toString()} data-testid = 'today-outfit-img'></img>
									</div>
									<div className="TodayOutfit-lable"
									data-testid = 'TodayOutfit-lable'>
										<text id="today-outfit-info-text">{userClothes.recommendOutfit.outfit_info}</text>
										{
											userClothes.recommendOutfit.userClothes.map((value, index) => {
												return(
													<div key={index}>
														<text id="today-cloth-name">{value.name}</text>
													</div>
												)
											})
										}
										{/*  */}
										<button id="wear-button" data-testid='wear-button'>오늘 입기</button>
									</div>
								</div>
								: <div></div>
							}
						</div>
					</div>
				</div>

				<div className="HomeBottom">
					<div className="OutfitDiv">
						<div className="OutfitHead">
							<text id="Outfit-text">Outfit</text>
							<button
								id="outfit-more-button"
								data-testid='more-btn'
								onClick={() => {
									navigate("/outfit");
								}}
							>
								More
							</button>
						</div>
						<div className="OutfitImage">
							{/*{codi_data_list.length > 2 ? (*/}
								<div className="Outfit-item-box"
								data-testid='OutfitPreview'>
									<OutfitPreview
										source_url={codi_data_list[0].codi_image}
										info={codi_data_list[0].explain}
										cloth_names={outfit_clothes[0].map((cloth) => {
											return cloth.cloth_name + " ";
										})}
									/>
									<OutfitPreview
										source_url={codi_data_list[1].codi_image}
										info={codi_data_list[1].explain}
										cloth_names={outfit_clothes[1].map((cloth) => {
											return cloth.cloth_name + " ";
										})}
									/>
									<OutfitPreview
										source_url={codi_data_list[2].codi_image}
										info={codi_data_list[2].explain}
										cloth_names={outfit_clothes[2].map((cloth) => {
											return cloth.cloth_name + " ";
										})}
									/>
								</div>
							{/*}) : (
								<div className="Outfit-item-box"
								data-testid='OutfitPreview'>
									{
										//codi_data_list.map((cloth, index)=>{
										//	<div id={index}>
										//		<OutfitPreview
										//			data-testid='OutfitPreview'
										//			source_url={cloth.codi_image}
										//		    info={cloth.explain}
										//			cloth_names={outfit_clothes[index].map((c, i)=>{
										//			return c.cloth_name + " "
										//		/>
										//	</div>
										//}
										//)
									}
								</div>
								)}*/}
						</div>
					</div>
				</div>
			</div>
		);
	}
}