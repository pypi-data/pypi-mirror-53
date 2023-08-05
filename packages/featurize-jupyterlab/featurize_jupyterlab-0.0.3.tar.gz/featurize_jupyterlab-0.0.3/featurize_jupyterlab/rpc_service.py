from . import constants as C
from .logger import get_runtime_logger

from .proto import minetorch_pb2, minetorch_pb2_grpc
from .experiment import Experiment


class MinetorchServicer(minetorch_pb2_grpc.MinetorchServicer):

    # TODO: performance of rpc server
    caches = {}

    timer_mapping = {
        C.TIMER_ITERATION: 1,
        C.TIMER_EPOCH: 2,
        C.TIMER_SNAPSHOT: 3,
    }

    def CreateGraph(self, request, context):
        # TODO: performance
        experiment, err = self._get_experiment(request.experiment_id)
        if not experiment:
            return err
        try:
            timer = experiment.timers.where(Timer.category == self.timer_mapping[request.timer_category]).get()
        except peewee.DoesNotExist:
            # TODO: here we should notify the user to create the timer first!
            return minetorch_pb2.StandardResponse(
                status=100,
                message='Timer does not exists, please create the correct timer before create graph'
            )
        try:
            Graph.create(
                experiment_id=experiment.id,
                snapshot_id=experiment.current_snapshot().id,
                name=request.graph_name,
                timer=timer
            )
        except peewee.IntegrityError:
            pass
        return minetorch_pb2.StandardResponse(
            status=0,
            message='ok'
        )

    def AddPoint(self, request, context):
        # TODO: performance
        experiment, err = self._get_experiment(request.experiment_id)
        if not experiment:
            return err
        graph = experiment.graphs.where(Graph.name == request.graph_name).get()
        graph.add_point(graph.timer.current, request.y)
        self.sio.emit('add_point', {
            'graph_id': graph.id,
            'graph_name': graph.name,
            'x': graph.timer.current,
            'y': request.y
        }, room=experiment.name, namespace='/common')
        return minetorch_pb2.StandardResponse(
            status=0,
            message='ok'
        )

    def SetTimer(self, request, context):
        # TODO: performance
        experiment, err = self._get_experiment(request.experiment_id)
        if not experiment:
            return err
        try:
            timer = experiment.timers.where(Timer.category == self.timer_mapping[request.category]).get()
            timer.current = request.current
            timer.save()
        except peewee.DoesNotExist:
            timer = Timer.create(
                experiment_id=experiment.id,
                snapshot_id=experiment.current_snapshot().id,
                category=self.timer_mapping[request.category],
                current=request.current,
                ratio=request.ratio
            )
        return minetorch_pb2.StandardResponse(
            status=0,
            message='ok'
        )

    def SendLog(self, request, context):
        # TODO: performance
        logger = get_runtime_logger(request.identity)
        getattr(logger, request.level.lower())(request.log)
        return minetorch_pb2.StandardResponse(
            status=0,
            message='ok'
        )

    def HeyYo(self, request, context):
        experiment = Experiment(request.identity)
        metadata = experiment.get_metadata()

        agent_status = request.status
        server_status = getattr(C, f"status_{metadata['status']}".upper())

        # Priority of status: Server Verb status > agent_status > server_status
        # TODO: find a way to set the status as not_running
        if server_status == C.STATUS_STARTING and agent_status == C.STATUS_IDLE:
            command = C.COMMAND_TRAIN
        elif server_status == C.STATUS_STOPPING and agent_status == C.STATUS_TRAINING:
            command = C.COMMAND_HALT
        elif server_status == C.STATUS_KILLING and agent_status == C.STATUS_IDLE:
            command = C.COMMAND_KILL
        else:
            experiment.update_metadata({
                'status': minetorch_pb2.HeyMessage.Status.Name(agent_status).lower()
            })
            command = C.COMMAND_NONE

        return minetorch_pb2.YoMessage(
            roger=True,
            command=command
        )
