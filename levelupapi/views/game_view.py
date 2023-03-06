"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Count
from django.db.models import Q
from django.core.exceptions import ValidationError
from levelupapi.models import Game, Gamer, GameType, Event


class GameView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        gamer = Gamer.objects.get(user=request.auth.user)


        try:
            game = Game.objects.annotate(
                event_count=Count('game_events'),
                user_event_count = Count('game_events', filter=Q(game_events__host=gamer))
            ).get(pk=pk)
            # game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)

        gamer = Gamer.objects.get(user=request.auth.user)

        games = Game.objects.annotate(
            event_count=Count('game_events'),
            user_event_count = Count('game_events', filter=Q(game_events__host=gamer))
        )

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        try:
            gamer = Gamer.objects.get(user=request.auth.user)
        except Gamer.DoesNotExist:
            return Response({'message': 'You sent an invalid token'}, status=status.HTTP_404_NOT_FOUND)

        game_type = GameType.objects.get(pk=request.data['game_type'])
        if game_type is None:
            return Response({'message': 'Please submit the game type. It cannot be blank.'}, status=status.HTTP_400_BAD_REQUEST)

        description = request.data.get('description', None)
        if description is None:
            return Response({'message': 'Please submit the description. It cannot be blank.'}, status=status.HTTP_400_BAD_REQUEST)
        
        game = Game.objects.create(
            name=request.data['name'],
            min_player=request.data['min_player'],
            description=request.data['description'],
            max_player=request.data['max_player'],
            gamer = gamer,
            game_type = game_type,
        )
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # def create(self, request):
    #     """Handle POST operations

    #     Returns:
    #         Response -- JSON serialized game instance
    #     """
    #     gamer = Gamer.objects.get(user=request.auth.user)
    #     serializer = CreateGameSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(gamer=gamer)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def update(self, request, pk):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        try:
            gamer = Gamer.objects.get(user=request.auth.user)
        except Gamer.DoesNotExist:
            return Response({'message': 'You sent an invalid token'}, status=status.HTTP_404_NOT_FOUND)

        game_type = GameType.objects.get(pk=request.data['game_type'])
        if game_type is None:
            return Response({'message': 'Please submit the game type. It cannot be blank.'}, status=status.HTTP_400_BAD_REQUEST)

        description = request.data.get('description', None)
        if description is None:
            return Response({'message': 'Please submit the description. It cannot be blank.'}, status=status.HTTP_400_BAD_REQUEST)
        
        game_to_update = Game.objects.get(pk=pk)
        game_to_update.name=request.data['name']
        game_to_update.min_player=request.data['min_player']
        game_to_update.description=request.data['description']
        game_to_update.max_player=request.data['max_player']
        game_to_update.gamer = gamer
        game_to_update.game_type = game_type
        game_to_update.save()
        
        serializer = GameSerializer(game_to_update)
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class GamerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gamer
        fields = ('id', )

class GameTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameType
        fields = ('id', 'label', )

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    event_count = serializers.IntegerField(default=None)
    user_event_count = serializers.IntegerField(default=None)
    gamer = GamerSerializer(many=False)
    game_type = GameTypeSerializer(many=False)

    class Meta:
        model = Game
        fields = ('id', 'name', 'description', 'game_type', 'min_player', 'max_player', 'gamer', 'event_count', 'user_event_count')
        depth = 1

class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'description', 'game_type', 'min_player', 'max_player']