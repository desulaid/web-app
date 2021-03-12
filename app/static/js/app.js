const addFormGroup = () => {
    const group = document.createElement("div")
    group.setAttribute("class", "input-group mb-3")

    return group
}

const addDeleteButton = (formId, groupFieldId) => {
    const button = document.createElement("button")
    button.type = "button"
    button.setAttribute("class", "btn btn-outline-danger")
    button.innerText = 'Удалить'
    button.onclick = () => {
        formId.removeChild(groupFieldId)
    }
    return button
}

const addInputField = (placeholder=null, value=null, id) => {
    const input = document.createElement("input")
    input.type = "text"
    input.setAttribute("name", `student-name-${id}`)
    input.setAttribute("class", "form-control")
    input.setAttribute("value", value)
    input.setAttribute("placeholder", placeholder)
    return input
};