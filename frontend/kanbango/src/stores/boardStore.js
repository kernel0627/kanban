// boardStore.js

import {ref} from 'vue'
import {defineStore} from 'pinia'
import axios from 'axios'

export const useBoardStore = defineStore('board', () =>{
    const boards = ref([])
    const currentBoard = ref(null)
    const isLoading = ref(false)

    async function fetchBoards(){
        isLoading.value = true
        try{
            const response = await axios.get('/boards')
            boards.value = response.data
        }catch(err){
            console.error('Error fetching boards:', err)
        }finally{
            isLoading.value = false
        }
    }

    async function fetchBoard(id){
        isLoading.value = true
        currentBoard.value = null
        try{
            const response = await axios.get(`/boards/${id}`)
            currentBoard.value = response.data
        }catch(err){
            console.error(`Failed to fetch board ${id}`, err)
        }finally{
            isLoading.value = false
        }
    }

    async function createBoard(title){
        try{
            const response = await axios.post('/boards', {title})
            boards.value.push(response.data)
            return response.data
        }catch(err){
            console.error('Failed to create board', err)
            throw err
        }
    }

    async function updateBoardTitle(boardId, newTitle) {
        try{
            await axios.put(`/boards/${boardId}`, { title: newTitle })
            const board = boards.value.find(b => b.id === boardId)
            if (board) {
                board.title = newTitle
            }
        }catch(err){
            console.error('Failed to update board title', err)
            throw err
        }
    }

    async function deleteBoard(boardId) {
        try{
            await axios.delete(`/boards/${boardId}`)
            const boardIndex = boards.value.findIndex(b => b.id === boardId)
            if (boardIndex !== -1) {
                boards.value.splice(boardIndex, 1)
                if (currentBoard.value?.id === boardId) {
                    currentBoard.value = null
                }
            }
        }catch(err){
            console.error('Failed to delete board', err)
            throw err
        }
    }

    async function createList(boardId,title){
        try{
            const response = await axios.post(`/boards/${boardId}/lists`, {title})
            if (currentBoard.value) {
                currentBoard.value.lists.push(response.data);
            }
        }catch(err){
            console.error('Failed to create board', err)
            throw err
        }
    }

    async function updateListTitle(listId, newTitle) {
        try {
            await axios.put(`/lists/${listId}`, { title: newTitle })
            const list = currentBoard.value?.lists.find(l => l.id === listId)
            if (list) {
                list.title = newTitle
            }
        } catch (err) {
            console.error('Failed to update list title', err)
            throw err
        }

    }

    async function deleteList(listId) {
        try {
            await axios.delete(`/lists/${listId}`)
            if (currentBoard.value) {
                const listIndex = currentBoard.value.lists.findIndex(l => l.id === listId)
                if (listIndex !== -1) {
                    currentBoard.value.lists.splice(listIndex, 1)
                }
            }
        } catch (err) {
            console.error('Failed to delete list', err)
            throw err
        }
    }


    async function createCard(listId,content){
        try{
            const response = await axios.post(`/lists/${listId}/cards`, {content})
            const list = currentBoard.value.lists.find(l => l.id === listId)

            if (list){
                if(!list.cards){
                    list.cards = []
                }
                list.cards.push(response.data)
            }
            return response.data
        }catch(err){
            console.error('Failed to create card', err)
            throw err
        }
    }

    async function updateCardContent(cardId, newContent) {
        try{
            await axios.put(`/cards/${cardId}` , {content: newContent})

            currentBoard.value.lists.forEach(list => {
                const card = list.cards?.find(c => c.id === cardId) 
                if (card) card.content = newContent
            })
        }catch(err){
            console.error('Failed to update card content', err)
            throw err
        }
    }

    async function deleteCard(listId , cardId) {
        try{
            await axios.delete(`/cards/${cardId}`)

            const list = currentBoard.value?.lists.find(l => l.id === listId)
            if(list) {
                const cardIndex = list.cards?.findIndex(c => c.id === cardId)
                if (cardIndex !== -1){
                    list.cards.splice(cardIndex, 1)
                }
            }
        }catch(err){
            console.error('Failed to delete card', err)
            throw err
        }
    }
    
    async function saveBoardStructure() {
        if (!currentBoard.value) return;
        try {
            const payload = {
                board_id: currentBoard.value.id,
                lists: currentBoard.value.lists.map(list => ({
                    id: list.id,
                    cards: list.cards.map(card => ({ id: card.id }))
                }))
            };
            await axios.put('/boards/update-order', payload);
        } catch (error) {
            console.error('Failed to save board structure:', error);
            alert('无法保存顺序，请刷新页面。');
        }
      }



    return {boards, currentBoard, isLoading, fetchBoards, fetchBoard, createBoard, createList, createCard , updateListTitle, deleteList , updateCardContent, deleteCard , updateBoardTitle, deleteBoard, saveBoardStructure}


})