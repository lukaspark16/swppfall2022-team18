import { fireEvent, render, screen } from "@testing-library/react";
import { Provider } from "react-redux";
// import { renderWithProviders } from "../../test-utils/mocks";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import ClothDetailModal from "./ClothDetailModal";
import { store } from "../../store";
import React from "react";
import { IProps as TypeFilterProps } from "../TypeFilter/TypeFilter";
import userEvent from "@testing-library/user-event";
// import DatePicker, { ReactDatePickerProps } from "react-datepicker";
// import { ReactDatePickerProps as DatePickerProps } from "react-datepicker";

const mockNavigate = jest.fn();
jest.mock("react-router", () => ({
	...jest.requireActual("react-router"),
	useNavigate: () => mockNavigate,
}));

const mockDispatch = jest.fn();
jest.mock("react-redux", () => ({
	...jest.requireActual("react-redux"),
	useDispatch: () => mockDispatch,
}));

// jest.mock(
// 	"react-datepicker",
// 	// eslint-disable-next-line react/display-name
// 	() => (props: ReactDatePickerProps) => (<div className="spyDatePicker" onChange={(clickedDate)=>void}>

//     </div>)
// );

jest.mock(
	"../TypeFilter/TypeFilter",
	// eslint-disable-next-line react/display-name
	() => (props: TypeFilterProps) =>
		(
			<div className="SpyFilterModal">
				<button
					id="done-button"
					data-testid="typefilter-done-button"
					onClick={() => props.selectHandler("")}
				>
					Done
				</button>
			</div>
		)
);

// jest.mock(
// 	"react-datepicker",
// 	// eslint-disable-next-line react/display-name
// 	() => (props: DatePickerProps) =>
// 		<div className="SpyDatePicker">DatePicker</div>
// );

{
	/* <DatePicker
dateFormat="yyyy/MM/dd"
highlightDates={highlightDates}
selected={wearDate}
onChange={(clickedDate: any) => setWearDateHandler(clickedDate)}
inline
/> */
}

describe("<ClothDetaillModal />", () => {
	let clothdetailmodal: JSX.Element;
	let clothdetailmodalWearDate: JSX.Element;

	beforeEach(() => {
		jest.clearAllMocks();
		clothdetailmodal = (
			<Provider store={store}>
				<MemoryRouter>
					<Routes>
						<Route
							path="/"
							element={
								<ClothDetailModal
									id="1"
									image="test"
									weardate=""
									metatype="아우터"
									type="트러커 재킷"
									color="그레이"
									pattern="None"
									modal_close={() => {
										console.log("something");
									}}
								/>
							}
						/>
					</Routes>
				</MemoryRouter>
			</Provider>
		);
		clothdetailmodalWearDate = (
			<Provider store={store}>
				<MemoryRouter>
					<Routes>
						<Route
							path="/"
							element={
								<ClothDetailModal
									id="1"
									image="test"
									weardate={'["2022/12/06"]'}
									metatype="아우터"
									type="트러커 재킷"
									color="그레이"
									pattern="None"
									modal_close={() => {
										console.log("something");
									}}
								/>
							}
						/>
					</Routes>
				</MemoryRouter>
			</Provider>
		);
	});
	it("should render without errors", () => {
		render(clothdetailmodal);
		screen.getByText("종류");
		screen.getByText("색상");
		screen.getByText("무늬");
		const moverecommendbutton = screen.getByText("Get Recommendation");
		fireEvent.click(moverecommendbutton);
		expect(mockNavigate).toHaveBeenCalledTimes(1);
	});

	it("should render with weardate", () => {
		render(clothdetailmodalWearDate);
		screen.getByText("종류");
		screen.getByText("색상");
		screen.getByText("무늬");
		const moverecommendbutton = screen.getByText("Get Recommendation");
		fireEvent.click(moverecommendbutton);
		expect(mockNavigate).toHaveBeenCalledTimes(1);
	});

	// it("should handle datePicker", () => {
	// 	render(clothdetailmodalWearDate);
	// 	const datePicker = screen.getByTestId("date-picker");
	// 	fireEvent.mouseDown(datePicker);
	// 	fireEvent.change(datePicker, { clickDate: "2022/12/03" });
	// });

	it("should handle edit clothes", () => {
		render(clothdetailmodal);
		const editButton = screen.getByText("Edit Cloth");
		fireEvent.click(editButton);
		const finishButton = screen.getByText("Finish Edit");
		fireEvent.click(finishButton);
	});

	it("should handle delete button", () => {
		render(clothdetailmodal);
		const deleteButton = screen.getByText("Delete Cloth");
		fireEvent.click(deleteButton);
	});

	it("should handle PatternOptionHandler", () => {
		render(clothdetailmodal);
		const editButton = screen.getByText("Edit Cloth");
		fireEvent.click(editButton);
		const selectElement = screen.getAllByRole("combobox", {})[0];
		userEvent.selectOptions(selectElement, "None");
		const defaultOption = screen.getByRole("option", {
			name: "Pattern",
		}) as HTMLOptionElement;
		const selectedOption = screen.getByRole("option", {
			name: "None",
		}) as HTMLOptionElement;
		fireEvent.click(selectedOption);
		expect(defaultOption.selected).toBeFalsy();
		expect(selectedOption.selected).toBeTruthy();
		fireEvent.click(defaultOption);
	});
	it("should handle PatternOptionHandler branch", () => {
		render(clothdetailmodal);
		const editButton = screen.getByText("Edit Cloth");
		fireEvent.click(editButton);
		const selectElement = screen.getAllByRole("combobox", {})[0];
		userEvent.selectOptions(selectElement, "Pattern");
		const defaultOption = screen.getByRole("option", {
			name: "Pattern",
		}) as HTMLOptionElement;
		expect(defaultOption.selected).toBeTruthy();
	});
});
