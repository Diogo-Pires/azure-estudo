module.exports = async function (context, req) {

    // We need both name and task parameters.
    if (req.query.prioridade && req.query.tarefa) {

        // Set the output binding data from the query object.
        context.bindings.tarefaDocument = req.query;

        // Success.
        context.res = {
            status: 200
        };
    }
    else {
        context.res = {
            status: 400,
            body: "The query options 'prioridade' and 'tarefa' are required."
        };
    }
};