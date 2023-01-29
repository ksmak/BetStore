let signUpForm = document.querySelector('.sign__up__form')
let signUpFormText = document.querySelector('.sign__up__form a')
let signUpFormInp = document.querySelector('.sign__up__form form')

signUpForm.addEventListener("mouseover", () => {
    signUpFormText.classList.add('disactive')
    signUpFormInp.classList.remove('disactive')
    signUpForm.addEventListener("mouseout", () => {
        signUpFormText.classList.remove('disactive')
        signUpFormInp.classList.add('disactive')
    })
})