"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType


class GameView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        game = Game.objects.all()
        serializer = GameSerializer(game, many=True)
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
    gamer = GamerSerializer(many=False)
    game_type = GameTypeSerializer(many=False)

    class Meta:
        model = Game
        fields = ('id', 'name', 'description', 'game_type', 'min_player', 'max_player', 'gamer')