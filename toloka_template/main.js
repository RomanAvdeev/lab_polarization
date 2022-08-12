let SOLVED_THRESHOLD = 10;
let UNSOLVED_MAX_RATIO = 0.5;

exports.Task = extend(TolokaHandlebarsTask, function (options) {
    TolokaHandlebarsTask.call(this, options);
}, {
    getSolution: function (solution) {
        let selected = this.getDOMElement().querySelector("input:checked");
        let output = {
            "task_id": this.getTask().id,
            "output_values": {
                "doc_id": this.getTask().input_values.id,
            }
        }
        if (selected) {
            output.output_values["pole"] = selected.value;
            output.output_values["pole_name"] = selected.labels[0]?.textContent; // была ошибка, что в поля нет label
        }
        return output
    },
    // validate: function (solution) {
    //     let selected = this.getDOMElement().querySelector("input:checked");
    //     let errors = null;
    //     if (!selected) {
    //         return {
    //             task_id: this.getTask().id,
    //             errors: {
    //                 '__TASK__': {
    //                     message: "Необходимо выбрать одно значение"
    //                 }
    //             }
    //         };
    //     } else {
    //         solution.output_values['pole'] = selected.value;
    //         solution.output_values['pole_name'] = selected.labels[0].textContent;
    //     }
    //     return TolokaHandlebarsTask.prototype.validate.apply(this, arguments);
    // },
    addError: function (message, field, errors) {
        errors || (errors = {
            task_id: this.getOptions().task.id,
            errors: {}
        });
        errors.errors[field] = {
            message: message
        };

        return errors;
    },
    onRender: function () {
        // DOM-элемент задания сформирован (доступен через #getDOMElement()) 
        const task = this.getDOMElement();
        const task_id = this.getTask().id;
        task.addEventListener('click', hideError);
        const addButton = task.querySelector("#add-pole")
        addButton.addEventListener('click', cloneOnClick.bind(null, task));

        task.querySelector(".task-id").value = task_id;

        task.querySelectorAll(".form-check-inline").forEach(elem => {
            let label = elem.querySelector("label");
            let radio = elem.querySelector("input");
            let newId = radio.getAttribute("id") + "_" + this.getTask().id
            label.setAttribute("for", newId);
            radio.setAttribute("id", newId);
            radio.setAttribute("name", task_id);
        })

        function formatId(taskId, topicId) {
            return "pole_" + taskId + "_" + topicId
        }

        function alert(task, message) {
            const placeholder = task.querySelector(".alert-placeholder")
            placeholder.innerHTML = '<div class="alert alert-warning alert-dismissible fade show" role="alert">' + message + '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>';
        }

        function removeButton() {
            // создание иконки с корзиной
            const div = document.createElement('div');
            div.style = "display: inline-block; cursor: pointer;";
            div.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16"><path fill-rule="evenodd" d="M6.5 1.75a.25.25 0 01.25-.25h2.5a.25.25 0 01.25.25V3h-3V1.75zm4.5 0V3h2.25a.75.75 0 010 1.5H2.75a.75.75 0 010-1.5H5V1.75C5 .784 5.784 0 6.75 0h2.5C10.216 0 11 .784 11 1.75zM4.496 6.675a.75.75 0 10-1.492.15l.66 6.6A1.75 1.75 0 005.405 15h5.19c.9 0 1.652-.681 1.741-1.576l.66-6.6a.75.75 0 00-1.492-.149l-.66 6.6a.25.25 0 01-.249.225h-5.19a.25.25 0 01-.249-.225l-.66-6.6z"></path></svg>';
            return div;
        }

        function onRadioRemove(radioContainer) {
            const radioName = radioContainer.querySelector("input").value;
            document.querySelectorAll("input[value='" + radioName + "']").forEach(e => e.parentElement.remove());
        }

        function cloneOnClick(task) {
            const poleName = task.querySelector(".pole-name");

            // закрываем все прошлые алерты
            $(task.querySelector(".alert")).alert("close");

            // валидация введенного названия
            if (!poleName.value.trim().length) {
                alert(task, "Название полюса не может быть пустым");
                return;
            }
            const existingRadios = new Set([...task.querySelectorAll("label")].map(x => x.textContent));
            if (existingRadios.has(poleName.value)) {
                alert(task, "Полюс с таким названием уже существует");
                return;
            }

            const wrappers = document.querySelectorAll(".classes")
            const firstTaskRadios = wrappers[0].querySelectorAll(".form-check-inline")
            const radioExample = firstTaskRadios[0];

            // берем максимальный из всех существующих id у радио кнопок (pole_{task_id}_{id})
            const existIds = [...firstTaskRadios].map(x => x.querySelector('input').id)
                .filter(x => x.startsWith("pole"))
                .map(x => parseInt(x.split("_").pop()));

            let topicId = 0;
            if (existIds.length > 0) {
                topicId = Math.max(...existIds) + 1;
            }

            wrappers.forEach(w => {
                const newElement = radioExample.cloneNode(true);
                const label = newElement.querySelector("label");
                const input = newElement.querySelector("input.form-check-input");
                const taskId = w.querySelector("input.task-id").value;
                const elementId = formatId(taskId, topicId);
                const removeIcon = removeButton();
                removeIcon.onclick = onRadioRemove.bind(null, newElement);

                label.setAttribute("for", elementId);
                label.textContent = poleName.value;
                input.setAttribute("id", elementId);
                input.setAttribute("value", "pole_" + topicId);
                input.setAttribute("name", taskId);
                newElement.appendChild(removeIcon);

                w.appendChild(newElement);
            });
            poleName.value = "";
        }

        function hideError({ target, currentTarget }) {
            const error = currentTarget.querySelector('.task__error');
            if (error && target.tagName === 'INPUT') {
                error.parentNode.removeChild(error);
            }
        }
    },
    onDestroy: function () {
        // Задание завершено, можно освобождать (если были использованы) глобальные ресурсы
    }
});


exports.TaskSuite = extend(TolokaHandlebarsTaskSuite, function (options) {
    TolokaHandlebarsTaskSuite.call(this, options);
}, {
    validate: function (solutions) {
        // TolokaTaskSuite.prototype.validate.call(this, solutions);

        let numSolved = 0;
        solutions.forEach(solution => {
            if (solution.output_values.pole && solution.output_values.pole_name) numSolved += 1;
        });
        if ((solutions.length <= SOLVED_THRESHOLD && numSolved === solutions.length) || (numSolved > SOLVED_THRESHOLD && numSolved / solutions.length > UNSOLVED_MAX_RATIO)) {
            return null;
        }
        let errors = [], tasks = this.getTasks();
        solutions.forEach((solution, i) => {
            if (!solution.output_values.pole || !solution.output_values.pole_name) {
                if (i < SOLVED_THRESHOLD || i / solutions.length < UNSOLVED_MAX_RATIO) {
                    errors.push(tasks[i].addError("Необходимо выбрать один из полюсов", "__TASK__"));
                }
            }
        });

        if (errors.length) {
            this.onValidationFail(errors);
            return errors;
        }
    }
});

function extend(ParentClass, constructorFunction, prototypeHash) {
    constructorFunction = constructorFunction || function () { };
    prototypeHash = prototypeHash || {};
    if (ParentClass) {
        constructorFunction.prototype = Object.create(ParentClass.prototype);
    }
    for (var i in prototypeHash) {
        constructorFunction.prototype[i] = prototypeHash[i];
    }
    return constructorFunction;
}
